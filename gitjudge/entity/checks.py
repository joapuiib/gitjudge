from gitjudge.entity import Commit

class Checks:
    def __init__(self):
        self.tags = []
        self.branches = []
        self.cherry_pick = None

    def __str__(self):
        args = []
        if self.tags:
            args.append(f"tags={self.tags}")
        if self.branches:
            args.append(f"branches={self.branches}")
        if self.cherry_pick:
            args.append(f"cherry_pick={self.cherry_pick}")
        return f"Checks({', '.join(args)})"

    def __repr__(self):
        return self.__str__()

    def validate(self, commit: Commit) -> bool:
        checks = {}
        if not isinstance(commit, Commit):
            raise TypeError("Checks.validate requires a Commit object")

        if self.tags:
            checks["tags"] = {}
            for tag in self.tags:
                if tag in commit.tags:
                    checks["tags"][tag] = True
                else:
                    checks["tags"][tag] = False

        if self.branches:
            checks["branches"] = {}
            for branch in self.branches:
                if branch in commit.branches:
                    checks["branches"][branch] = True
                else:
                    checks["branches"][branch] = False

        return checks
