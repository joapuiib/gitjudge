from gitjudge.entity import Commit
from gitjudge.entity.checks import Check

class RevertsCheck(Check):
    def __init__(self, reference):
        self.reference = reference


    def __str__(self):
        return f"RevertsCheck(reference={reference})"


    def __repr__(self):
        return self.__str__()


    def resolve_references(self, commit_id, resolver):
        self.reference = resolver.resolve_reference(commit_id, self.reference)


    def validate(self, commit: Commit) -> bool:
        super().validate(commit, repo)

        self.correct = commit.reverts(self.reference)

        return self.correct
