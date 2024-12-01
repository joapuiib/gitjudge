from gitjudge.entity.commit import Commit


class Check:
    def __init__(self):
        self.checked = False
        self.correct = False

    def __str__(self):
        return "Check()"

    def __repr__(self):
        return self.__str__()

    def resolve_references(self, commit_id, resolver):
        pass

    def validate(self, commit: Commit, repo) -> bool:
        if not isinstance(commit, Commit):
            raise TypeError("Checks.validate requires a Commit object")

        self.checked = True
        self.correct = True
        return self.correct
