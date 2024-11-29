from gitjudge.entity import Commit
from gitjudge.entity.checks import Check

class TagCheck(Check):
    def __init__(self, tags=[]):
        self.tags = {}
        for tag in tags:
            self.tags[tag] = False


    def __str__(self):
        return f"TagCheck({self.tags})"


    def __repr__(self):
        return self.__str__()


    def validate(self, commit, repo) -> bool:
        if not isinstance(commit, Commit):
            raise TypeError("Checks.validate requires a Commit object")

        correct = True
        for tag in self.tags.keys():
            tag_present = tag in commit.tags
            self.tags[tag] = tag_present
            correct = correct and tag_present

        return correct
