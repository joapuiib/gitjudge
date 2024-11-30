from gitjudge.entity.commit import Commit

from .check import Check


class BranchCheck(Check):
    def __init__(self, branches=[]):
        self.branches = {}
        for branch in branches:
            self.branches[branch] = False

    def __str__(self):
        return f"BranchCheck({self.branches})"


    def __repr__(self):
        return self.__str__()


    def validate(self, commit, repo) -> bool:
        super().validate(commit, repo)

        for branch in self.branches.keys():
            branch_present = branch in commit.branches
            self.branches[branch] = branch_present
            self.correct = self.correct and branch_present

        return self.correct
