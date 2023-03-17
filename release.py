import os
import subprocess
import shutil
import requests

from github import Github
from github import InputFileContent
import git
from src import constants as cons


class Release:
    def __init__(self, github_user, repo_name):
        print(cons.TOKEN)
        self.github = Github(cons.TOKEN)
        self.github_user = github_user
        self.repo_name = repo_name
        self.repo = self.github.get_repo(f"{self.github_user}/{self.repo_name}")

    def create_release(self):
        self.create_version()
        self.create_exe()
        self.create_github_release()
        self.clean_up()

    def create_version(self):
        try:
            self.current_version = self.repo.get_latest_release().tag_name
            major, minor, patch = map(int, self.current_version.split("."))
            patch += 1
            if patch > 9:
                minor += 1
                patch = 0

            if minor > 9:
                major += 1
                minor = 0

            self.version = f"{major}.{minor}.{patch}"
        except:
            self.version = "1.0.0"

        self.current_release = f"{self.repo_name} v{self.version}"
        self.release_name = f"{self.repo_name} v{self.version}"
        return self.current_release

    def create_exe(self):
        subprocess.call("pyinstaller release.spec", shell=True)

        for item in os.listdir("dist"):
            new_name = f"{self.release_name}.exe"
            shutil.move(os.path.join("dist", item), new_name)
            self.exe_path = new_name

    def create_github_release(self):
        print(f"Creating release for {self.repo_name} v{self.version}")
        release = self.repo.create_git_release(
            tag=self.version,
            name=self.release_name,
            message=f"Release bundled exe for {self.repo_name}",
        )

        asset = release.upload_asset(path=self.exe_path, label=self.release_name)

    def clean_up(self):
        print("Cleaning up")
        shutil.rmtree("dist")
        shutil.rmtree("build")
        os.remove(self.exe_path)


Release("tdanbo", "VanguardCS").create_release()
