from gitjudge.entity.checks import Check

class TagCheck(Check):
    def __init__(self):
        self.tags = []


    def __str__(self):
        return f"TagCheck({self.tags})"


    def __repr__(self):
        return self.__str__()


    def validate(self, commit) -> bool:
        if not isinstance(commit, Commit):
            raise TypeError("Checks.validate requires a Commit object")

        correct = True
        for tag in self.tags:
            tag_present = tag in commit.tags
            correct = correct and tag_present

        return correct
