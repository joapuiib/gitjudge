from gitjudge.entity.commit import Commit, DiffList
from gitjudge.entity.difflist import DiffList

from .check import Check


class DiffCheck(Check):
    def __init__(self, diff: DiffList):
        self.diff = diff


    def __str__(self):
        return f"DiffCheck({self.diff})"


    def __repr__(self):
        return self.__str__()


    def validate(self, commit, repo) -> bool:
        super().validate(commit, repo)

        self.correct = commit.diff.contains(self.diff)

        return self.correct
