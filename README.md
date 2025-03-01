# Push Docker Hub Overview

## Version

**v1.0.1** 🚀

## Description
I created this script to automate the process of pushing an overview (similar to README.md) to a Docker Hub repository in an easy way. The main goal is to use it in a CI/CD pipeline.

You provide the script with your username, password or PAT (Personal Access Token), the repository, and your overview either through a file or text via the command line.

## Usage
1. First, clone the repository and navigate to the directory:
    ```sh
    git clone https://github.com/Nemesix493/PushDockerHubOverview.git && cd PushDockerHubOverview/
    ```
2. Create your virtual environment:
    ```sh
    python -m venv env
    ```
3. Install the dependencies:
    ```sh
    env/bin/pip install -r ./requirements.txt
    ```
4. Run the script:
    ```sh
    env/bin/python -m main -u <USERNAME> -r <REPOSITORY> (-p <PASSWORD> | -t <TOKEN>) (-f <FILE> | -o <OVERVIEW>)
    ```

## Script Workflow

1. Load and check arguments.
2. Instantiate the [API object](docker_hub_api.py).
3. Get the JWT from API authentication.
4. Use the JWT to update the overview via the PATCH method.