from gitjudge.entity.commit import Commit

from .check import Check


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
        super().validate(commit, repo)

        for tag in self.tags.keys():
            tag_present = tag in commit.tags
            self.tags[tag] = tag_present
            self.correct = self.correct and tag_present

        return self.correct
