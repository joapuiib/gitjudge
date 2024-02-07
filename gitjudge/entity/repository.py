import os
import git
import subprocess

from gitjudge.entity import Definition, ExpectedCommit, Commit

class Repository:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        if not os.path.isdir(directory_path):
            raise ValueError("Path does not exist")

        self.repo = git.Repo(directory_path)

    def log(self):
        git_log_command = "git log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all"
        result = subprocess.run(git_log_command, cwd=self.directory_path, shell=True, capture_output=True, text=True)
        return result.stdout


    def find_commit(self, expected_commit, parent_commit=None):
        """
        Find a commit in the repository that matches the expected commit.

        The search will start from the `starting_point` commit ('HEAD' by default),
        so it will find the most recent commit that matches the expected commit.

        If a parent commit is provided, the search will stop at the parent commit.

        None is returned if:
            - The repository is empty
            - The commit is not found

        The commit to be found is considered a match if:
            - The commit is tagged with the expected tags (if any)
            - The commit message starts with the expected commit message
        """
        if not isinstance(expected_commit, ExpectedCommit):
            raise TypeError("Expected a ExpectedCommit object")
        if parent_commit is not None and not isinstance(parent_commit, Commit):
            raise TypeError("Parent commit expected a Commit object")

        # If the repository is empty, there are no commits to find
        if not self.repo.active_branch.is_valid():
            return None

        rev = expected_commit.starting_point or "HEAD"
        if parent_commit is not None:
            rev = f"{parent_commit.hash}..{rev}"

        commit_found = None
        for commit in self.repo.iter_commits(rev=rev):
            if commit.message.lower().startswith(expected_commit.message.lower()):
                commit_found = commit
                break

        if commit_found is not None:
            result = Commit(expected_commit.id)
            result.message = commit_found.message.strip()
            result.hash = commit_found.hexsha
            return result
        return None
