from gitjudge.entity import Commit

class Checks:
    def __init__(self):
        self.tags = []
        self.branches = []
        self.cherry_pick = None
        self.reverts = None

    def __str__(self):
        args = []
        if self.tags:
            args.append(f"tags={self.tags}")
        if self.branches:
            args.append(f"branches={self.branches}")
        if self.cherry_pick:
            args.append(f"cherry_pick={self.cherry_pick}")
        if self.reverts:
            args.append(f"reverts={self.reverts}")
        return f"Checks({', '.join(args)})"

    def __repr__(self):
        return self.__str__()

    def validate(self, commit: Commit, found_commits:dict = {}) -> bool:
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

        if self.cherry_pick:
            referenced_commit = found_commits.get(self.cherry_pick)
            if not referenced_commit:
                checks["cherry_pick"] = False
            else:
                checks["cherry_pick"] = commit.is_cherry_picked_from(referenced_commit)

        if self.reverts:
            referenced_commit = found_commits.get(self.cherry_pick)
            if not referenced_commit:
                checks["reverts"] = False
            else:
                checks["reverts"] = commit.reverts(referenced_commit)

        # TODO: Implement revert checks
        return checks
