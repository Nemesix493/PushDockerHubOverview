from urllib.parse import urljoin

import requests


class DockerHubAPI:
    API_HOST = 'https://hub.docker.com/v2/'
    AUTH_URI = urljoin(API_HOST, 'auth/token')
    REPOSITORIES_URI = urljoin(API_HOST, 'repositories/')

    def __init__(self, docker_hub_username: str,
                 docker_hub_password: str | None = None,
                 docker_hub_pat: str | None = None
                 ):
        if docker_hub_password is None and docker_hub_pat is None:
            raise ValueError(
                "docker_hub_password and docker_hub_pat cannot be both None"
            )
        self._docker_hub_username = docker_hub_username
        self._docker_hub_password = docker_hub_password
        self._docker_hub_pat = docker_hub_pat
        self._jwt = None

    @property
    def docker_hub_username(self) -> str:
        return self._docker_hub_username

    @property
    def docker_hub_password(self) -> str | None:
        return self._docker_hub_password

    @property
    def docker_hub_pat(self) -> str | None:
        return self._docker_hub_pat

    @property
    def jwt(self) -> str:
        if self._jwt is None:
            self._get_jwt()
        return self._jwt

    def _get_jwt(self) -> None:
        if self._docker_hub_pat is not None:
            response = self._get_docker_hub_jwt_pat()
        else:
            response = self._get_docker_hub_jwt_pwd()
        response.raise_for_status()
        self._jwt = response.json()['access_token']

    def _get_docker_hub_jwt_pwd(self) -> requests.Response:
        return requests.post(
            url=self.AUTH_URI,
            headers={
                'Content-type': 'application/json'
            },
            json={
                'username': self._docker_hub_username,
                'password': self._docker_hub_password
            }
        )

    def _get_docker_hub_jwt_pat(self) -> requests.Response:
        return requests.post(
            url=self.AUTH_URI,
            headers={
                'Content-type': 'application/json'
            },
            json={
                'identifier': self._docker_hub_username,
                'secret': self._docker_hub_pat
            }
        )

    def push_overview(self, repo_name: str, overview: str) -> requests.Response:
        response = requests.patch(
            url=urljoin(self.REPOSITORIES_URI, f"{self._docker_hub_username}/{repo_name}/"),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.jwt}'
            },
            json={
                'full_description': str(overview)
            }
        )
        response.raise_for_status()
        return response
