import os
import shutil
import subprocess


def is_github_url(url):
    return "github.com" in url


def clone_repository(url, directory):
    subprocess.check_call(["git", "clone", url, directory])


def process_repository(repo_directory):
    if not os.path.exists("gpt-repository-loader"):
        clone_repository("https://github.com/mpoon/gpt-repository-loader", "gpt-repository-loader")

    absolute_repo_directory = os.path.abspath(repo_directory)

    subprocess.check_call(["python3", "gpt_repository_loader.py", absolute_repo_directory, "-o", "output.txt"],
                          cwd="gpt-repository-loader")

    with open("gpt-repository-loader/output.txt", "r") as f:
        return f.read()


def remove_repositories(repo_directory):
    try:
        shutil.rmtree(repo_directory)
    except FileNotFoundError:
        print(f"Warning: {repo_directory} not found")

    try:
        shutil.rmtree("gpt-repository-loader")
    except FileNotFoundError:
        print("Warning: gpt-repository-loader not found")
