from gitjudge.entity import Commit, CheckResult
from gitjudge.common.utils import resolve_commit_reference

class ExpectedCommit:
    def __init__(self, id: str, message: str = None, start: str = None, end: str = None):
        self.id = id
        self.message = message
        self.start = start
        self.end = end

        self.parents = []
        self.branches = []
        self.tags = []

        self.checks = None

    def set_message(self, message):
        self.message = message

    def add_branch(self, branch):
        self.branches.append(branch)

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_parent(self, parent):
        self.parents.append(parent)

    def __str__(self):
        args = []
        args.append(f"id={self.id}")
        if self.message:
            args.append(f"message={self.message}")
        if self.start:
            args.append(f"start={self.start}")
        if self.end:
            args.append(f"end={self.end}")
        if self.checks:
            args.append(f"checks={self.checks}")
        return f"ExpectedCommit({', '.join(args)})"

    def __repr__(self):
        return self.__str__()

    def resolve_references(self, found_commits: dict = {}):
        resolve_commit_reference(self, self.id, 'start', found_commits)
        resolve_commit_reference(self, self.id, 'end', found_commits)

        if self.checks:
            self.checks.resolve_references(self.id, found_commits)


    def validate(self, commit: Commit) -> bool:
        if not isinstance(commit, Commit):
            raise TypeError("ExpectedCommit.validate requires a Commit object")

        if self.checks:
            return self.checks.validate(commit)

        return CheckResult(commit)
