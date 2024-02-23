import os
import git
import subprocess
import re

from gitjudge.entity import Definition, ExpectedCommit, Commit, NotFoundCommit, ReferencedItselfCommit

class Repository:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        if not os.path.isdir(directory_path):
            raise ValueError("Path does not exist")

        self.repo = git.Repo(directory_path)


    def log_command(self, start=None, end=None, branches=None, all=False):
        git_log_command = "git log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)'" # --all"

        if start is not None and end is not None:
            short_start = start.short_hash()
            short_end = end.short_hash()
            git_log_command = git_log_command + f" --ancestry-path {short_start}~1..{short_end}"
        elif start is not None:
            short_start = start.short_hash()
            git_log_command = git_log_command + f" {short_start}"
        elif end is not None:
            short_end = end.short_hash()
            git_log_command = git_log_command + f"..{short_end}"

        if branches is not None:
            git_log_command = git_log_command + " " + " ".join(branches)

        if all:
            git_log_command = git_log_command + " --all"


        return git_log_command

    def log(self, start=None, end=None, branches=None, all=False):
        git_log_command = self.log_command(start, end, branches, all)
        result = subprocess.run(git_log_command, cwd=self.directory_path, shell=True, capture_output=True, text=True)
        return result.stdout

    def print_log(self, start=None, end=None, branches=None, all=False):
        git_log_command = self.log_command(start, end, branches, all)
        subprocess.run(git_log_command, cwd=self.directory_path, shell=True)
        print("")


    # Not unit tested, but tested in find_commit
    def get_tags_for_commit(self, commit: git.Commit):
        tags = []
        for tag in self.repo.tags:
            if tag.commit.hexsha == commit.hexsha:
                tags.append(tag.name)
        return tags


    def _create_commit(self, commit: git.Commit, id=None):
        result = Commit(id)
        result.message = commit.message.strip()
        result.hash = commit.hexsha
        result.tags = self.get_tags_for_commit(commit)
        result.comitted_date = commit.committed_datetime

        show_output = self.repo.git.show(commit.hexsha, color='always')
        diff_start = show_output.find('@@')
        result._diff = ""
        if diff_start != -1:
            result._diff = show_output[diff_start:]

        return result


    def find_commit_by_ref(self, ref):
        if ref in self.repo.refs:
            return self._create_commit(self.repo.commit(ref), ref)

        return NotFoundCommit(ref)


    def find_commits_in_branch(self, branch, end=None):
        if end is not None:
            if isinstance(end, Commit):
                end = end.hash
            end = self.repo.commit(end)
        else:
            end = self.repo.commit("HEAD")

        common_ancestor = self.repo.merge_base(branch, end)[0]

        commits = []
        for commit in self.repo.iter_commits(rev=f"{common_ancestor}..{branch}", reverse=True):
            commits.append(self._create_commit(commit))

        return commits



    def find_commit(self, expected_commit):
        """
        Find a commit in the repository that matches the expected commit.

        The search will start from the `start` ref ('HEAD' by default),
        so it will find the most recent commit that matches the expected commit.

        If `end` is provided, the search will be limited to the commits between `start` and `end`.

        If `start` and `end` are provided, but `start` is an ancestor of `end`, the search will be reversed
        and the oldest commit that matches the expected commit will be found, limited to the commits between `start` and `end`.

        None is returned if:
            - The repository is empty
            - The commit is not found

        The commit to be found is considered a match if:
            - The commit is tagged with the expected tags (if any) (Not implemented yet)
            - The commit message starts with the expected commit message
        """
        if not isinstance(expected_commit, ExpectedCommit):
            raise TypeError("Expected a ExpectedCommit object")

        # If the repository is empty, there are no commits to find
        if not self.repo.active_branch.is_valid():
            return None

        start = expected_commit.start

        if isinstance(start, NotFoundCommit):
            return NotFoundCommit(expected_commit.id)
        if isinstance(start, ReferencedItselfCommit):
            return ReferencedItselfCommit(expected_commit.id)

        if isinstance(expected_commit.start, Commit):
            start = start.hash
        start = self.repo.commit(start or "HEAD")

        end = expected_commit.end

        if isinstance(end, NotFoundCommit):
            return NotFoundCommit(expected_commit.id)
        if isinstance(end, ReferencedItselfCommit):
            return ReferencedItselfCommit(expected_commit.id)

        if isinstance(expected_commit.end, Commit):
            end = end.hash

        if end is not None:
            end = self.repo.commit(end)

        reverse_search = False
        if end is not None:
            common_ancestor = self.repo.merge_base(start, end)
            if common_ancestor:
                common_ancestor = common_ancestor[0]
                # start is older than end
                if common_ancestor.hexsha == start.hexsha:
                    reverse_search = True
                    aux = start
                    start = end
                    end = aux
                # start is newer than end
                elif common_ancestor.hexsha == end.hexsha:
                    reverse_search = False
                else:
                    raise ValueError("Start and end are not related")

        rev = start
        if end is not None:
            rev = f"{end}..{start}"

        list_commits = list(self.repo.iter_commits(rev=rev, reverse=reverse_search))
        if end is not None:
            if reverse_search:
                list_commits.insert(0, self.repo.commit(end))
            else:
                list_commits.append(self.repo.commit(end))

        commit_found = None
        for commit in list_commits:
            expected_commit_pattern = re.compile("^" + expected_commit.message + ".*", re.IGNORECASE)
            if re.match(expected_commit_pattern, commit.message.strip()):
                commit_found = commit
                break

        if commit_found is not None:
            return self._create_commit(commit_found, expected_commit.id)

        return NotFoundCommit(expected_commit.id)
