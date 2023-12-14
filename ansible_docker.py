#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action to upload ansible roles to galaxy.ansible.com (galaxy-ng)
"""
import subprocess
import os
import sys
from urllib.parse import urlparse

class EnvironmentManager:
    """
    Parsing Enviroment Variables
    """
    def __init__(self, env_var_name):
        self.env_var_name = env_var_name
        self.env_var_value = os.getenv(env_var_name)

    def check_optional_environment_variable_with_default(self):
        """
        Check if optional variable with defaukt value is defined.
        """
        if self.env_var_value is not None:
            print(f"The value of {self.env_var_name} is: {self.env_var_value}")
            return f"{self.env_var_value}"
        print(f"The variable {self.env_var_name} is not set.")
        print("But a default value should have be defined.\nSomething is wrong. CANCEL")
        sys.exit(1)

    def check_optional_environment_variable_without_default(self):
        """
        Check if optional Variable is defined.
        """
        if self.env_var_value is not None:
            print(f"The value of {self.env_var_name} is: {self.env_var_value}")
            return f"{self.env_var_value}"
        print(f"The variable {self.env_var_name} is not set.")
        return ""

    def check_secret_environment_variable(self):
        """
        Check if required Variable is defined.
        exit if undefined
        """
        if self.env_var_value is not None:
            print(f"The value of {self.env_var_name} is defined")
            return f"{self.env_var_value}"
        print(f"The variable {self.env_var_name} is not set but needs to be defined.\nFAILED")
        sys.exit(1)

# pylint: disable=R0903
class AnsibleCommandExecution:
    """
    running ansible galaxy command
    """
    def run_command(self, command):
        """
        Running command as subprocess.
        Printing error on fail and exit
        """
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as error:
            print(f"Error running Ansible command: {error}\n\n{error.stdout}\n{error.stderr}")
            sys.exit(1)

def is_url(string):
    """
    Check if a string is a valid url, using urlparse
    """
    try:
        result = urlparse(string)
        print(result)
        return str(string)
    except ValueError:
        print(f"{string} is not a valid URL.\nCANCEL")
        sys.exit(1)

def write_ansible_galaxy_config(galaxy_api_key_value, galaxy_api_value):
    """
    writing ansible galaxy config to file
    """
    content = f"""
[galaxy]
server_list = galaxy

[galaxy_server.galaxy]
url = {galaxy_api_value}
token = {galaxy_api_key_value}
"""

    file_path = "/etc/ansible/galaxy.cfg"
    directory_path = '/etc/ansible/'

    # Check if the directory exists, and if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Inhalt in die Datei schreiben
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f'Die Config wurde erfolgreich als Datei "{file_path}" geschrieben.')

if __name__ == "__main__":
    # define known enviroment vars
    ENV_GALAXY_API_KEY_NAME = "GALAXY_API_KEY"
    ENV_GIT_BRANCH_NAME = "GIT_BRANCH"
    ENV_PATH_NAME = "PATH"
    ENV_GALAXY_API_NAME = "GALAXY_API"

    # check for galaxy_api_key variable
    env_galaxy_api_key = EnvironmentManager(ENV_GALAXY_API_KEY_NAME)
    galaxy_api_key = env_galaxy_api_key.check_secret_environment_variable()
    if galaxy_api_key == "":
        print("galaxy_api_key needs to be defined")
        sys.exit(1)

    # check for git_branch variable
    env_git_branch = EnvironmentManager(ENV_GIT_BRANCH_NAME)
    git_branch_check = env_git_branch.check_optional_environment_variable_without_default()
    if git_branch_check == "":
        print("Using main as git_branch")
        git_branch = 'main'
    else:
        git_branch = git_branch_check

    # check for path variable
    env_path = EnvironmentManager(ENV_PATH_NAME)
    path = env_path.check_optional_environment_variable_with_default()
    if path == "":
        print("path needs to be defined")
        sys.exit(1)

    # check for galaxy_api variable
    env_galaxy_api = EnvironmentManager(ENV_GALAXY_API_NAME)
    galaxy_api_url = env_galaxy_api.check_optional_environment_variable_with_default()
    # pylint: disable=C0103
    galaxy_api = str(is_url(galaxy_api_url))
    if galaxy_api == "":
        print("galaxy_api needs to be defined")
        print(f"galaxy api is {galaxy_api}, default is 'https://galaxy.ansible.com/api/'.")
        sys.exit(1)

    # define git repo ans user/organisation
    github_repository_env = EnvironmentManager('GITHUB_REPOSITORY')
    github_repository = github_repository_env.check_optional_environment_variable_with_default()
    gh_parts = github_repository.split('/')

    github_organisation = gh_parts[0]
    github_repo = gh_parts[1]

    # config for galaxy
    write_ansible_galaxy_config(f"{galaxy_api_key}", f"{galaxy_api}")

    # execute linting commands
    execute = AnsibleCommandExecution()

    # run ansible galaxy
    import_command = ["/usr/local/bin/ansible-galaxy", "role", "import", "-vvv", "--api-key",
      f"{galaxy_api_key}", "--branch", f"{git_branch}", f"{github_organisation}", f"{github_repo}"]
    upload_run = execute.run_command(import_command)
    upload_result = f"""
---start+galaxy-ng+role+upload---
/usr/local/bin/ansible-galaxyrole import -vvv \\
    --api-key *********** \\
    --branch {git_branch} \\
    {github_organisation} {github_repo}
{upload_run}
Galaxy upload run executed
---end+galaxy-ng+role+upload---
"""
    print(upload_result)
