import configparser
import json
import logging
import os
from pathlib import Path
import random
import requests
import string
import subprocess
import tarfile


logging.basicConfig(filename='runner-connect.log', level=logging.DEBUG)
CONFIG = configparser.ConfigParser()
CONFIG.read('/Users/admin/agent/runner_connect.cfg')
PATH_TO_RUNNER = CONFIG['runner']['path']

class GitHubActionsRunnerConnect:
    def __init__(self):
        self.api_base_url = CONFIG['github']['api_base_url']
        self.headers = {'Accept':'application/vnd.github.v3+json'}
        self.token = None
        orka_node_name = requests.get('http://169.254.169.254/metadata/orka_node_name')
        self.orka_node_name = orka_node_name
        vm_name = requests.get('http://169.254.169.254/metadata/orka_vm_name')
        self.vm_name = json.loads(vm_name._content.decode("utf-8"))['value']
        github_user = requests.get('http://169.254.169.254/metadata/github_user')
        self.github_user = json.loads(github_user._content.decode("utf-8"))['value']
        github_pat = requests.get('http://169.254.169.254/metadata/github_pat')
        self.github_pat = json.loads(github_pat._content.decode("utf-8"))['value']
        github_repo_name = requests.get('http://169.254.169.254/metadata/github_repo_name')
        self.github_repo_name = json.loads(github_repo_name._content.decode("utf-8"))['value']
        self.gh_session = requests.Session()
        self.gh_session.auth = (self.github_user, self.github_pat)

    def check_for_runner(self):
        Path(PATH_TO_RUNNER).mkdir(parents=True, exist_ok=True)
        runner_installed = False
        if 'bin' in os.listdir(PATH_TO_RUNNER):
            runner_installed = True
        print(runner_installed) 
        return runner_installed

    def install_runner(self):
        download_url = CONFIG['github']['runner_download_url']
        split_path = os.path.split(download_url)
        filename = split_path[1]
        filepath = os.path.join(PATH_TO_RUNNER, filename)
        r = requests.get(download_url, allow_redirects=True)
        with open(filepath, 'wb') as download:
            download.write(r.content)
        tar = tarfile.open(filepath)
        tar.extractall(PATH_TO_RUNNER)

    def _build_get_token_request_url(self):
        try:
            return f"{self.api_base_url}repos/{self.github_user}/{self.github_repo_name}/actions/runners/registration-token"
        except Exception as e:
            logging.error(str(e))

    def generate_token(self):
        try:
            url = self._build_get_token_request_url()
            response = self.gh_session.post(url, headers=self.headers)
            response = json.loads(response._content)
            self.token = response['token']
            print(self.token)
            log = f"Token created: {self.token}"
            logging.info(log)
        except Exception as e:
            logging.error(str(e))

    # def _create_runner_name(self):
    #     letters = string.ascii_lowercase
    #     prefix = CONFIG['runner']['name']
    #     suffix = ''.join(random.choice(letters) for i in range(10))
    #     return f"{prefix}-{suffix}"

    def register_runner(self):
        try:
            repo_url = f"https://github.com/{self.github_user}/{self.github_repo_name}"
            labels = self.vm_name
            runner_path = PATH_TO_RUNNER
            config_path = os.path.join(runner_path, 'config.sh')
            cmd = [config_path, '--url', repo_url, '--token', self.token, '--name', self.vm_name, '--work', '_work', '--labels', labels]
            response = subprocess.run(cmd, capture_output=True)
            logging.info(f"RUNNER-NAME: {self.vm_name}")
            logging.info(str(response.stdout))
        except Exception as e:
            logging.error(str(e))

    def start_runner(self):
        try:
            runner_path = PATH_TO_RUNNER
            start_path = os.path.join(runner_path, 'run.sh')
            subprocess.Popen(start_path, shell=True)
            logging.info('Runner started.')
        except Exception as e:
            logging.error(str(e))

if __name__ == '__main__':
    runner_connect = GitHubActionsRunnerConnect()
    if runner_connect.check_for_runner():
        print('runner found')
        runner_connect.generate_token()
        print('token generated')
        print(runner_connect.token)
        runner_connect.register_runner()
        print('runner registered')
        runner_connect.start_runner()
        print('runner started')
    else:
        print('runner NOT found')
        runner_connect.install_runner()
        print('runner installed')
        runner_connect.generate_token()
        print('token generated')
        runner_connect.register_runner()
        print('runner registered')
        runner_connect.start_runner()
        print('runner started')