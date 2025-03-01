import argparse
from pathlib import Path

from docker_hub_api import DockerHubAPI


def load_overview_file(overview_file_path: Path) -> str:
    with open(overview_file_path, 'r', encoding='utf-8') as overview_file:
        return overview_file.read()


def main():
    parser = argparse.ArgumentParser(
        description="This script allows you to push a Docker Hub repository overview via the API.\n"
        "Password or token is required but not both.\n"
        "Overview or file is required but not both."
    )
    parser.add_argument("-u", "--username", required=True, help="Docker Hub username (required)")
    parser.add_argument("-r", "--repository", required=True, help="Docker Hub repository name (required)")

    # Secret args
    authentication_group = parser.add_mutually_exclusive_group(required=True)
    authentication_group.add_argument("-p", "--password", help="Docker Hub password (required or token)")
    authentication_group.add_argument(
        "-t",
        "--token",
        help="Docker Hub Personnnal Access Token PAT (required or password)"
    )

    # Overview args
    overview_group = parser.add_mutually_exclusive_group(required=True)
    overview_group.add_argument(
        "-f",
        "--overview-file",
        dest="file",
        help="Path to overview file (required or overview-text)"
    )
    overview_group.add_argument(
        "-o",
        "--overview-text",
        dest="overview",
        help="Overview text(required or overview-file)"
    )
    args = parser.parse_args()

    # Use password or token depending of which given
    if args.token:
        api = DockerHubAPI(
            docker_hub_username=args.username,
            docker_hub_pat=args.token
        )
    else:
        api = DockerHubAPI(
            docker_hub_username=args.username,
            docker_hub_password=args.password
        )

    # Use overview file or overview text depending of which given
    if args.file:
        file_path = Path(args.file).resolve()
        if file_path.exists() and file_path.is_file():
            overview = load_overview_file(file_path)
        else:
            raise ValueError(f"The path to the overview file given is incorrect : {args.file}")
    else:
        overview = args.overview

    # Push overview to Docker Hub
    api.push_overview(args.repository, overview)


if __name__ == '__main__':
    main()
