from gitjudge.entity import Commit
from gitjudge.entity.checks import Check

class SquashCheck(Check):
    def __init__(self, references: list):
        self.references = references


    def __str__(self):
        return f"SquashCheck(reference={reference})"


    def __repr__(self):
        return self.__str__()


    def resolve_references(self, commit_id, resolver):
        for i, r in enumerate(self.references):
            self.references[i] = resolver.resolve_reference(commit_id, r)


    def validate(self, commit: Commit) -> bool:
        super().validate(commit, repo)

        self.correct = commit.squashes(self.squashes)

        return self.correct
