from gitjudge.entity import Commit, CheckResult

class Checks:
    def __init__(self):
        self.tags = []
        self.branches = []
        self.cherry_pick = None
        self.reverts = None
        self.squashes = None


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
        if self.squashes:
            args.append(f"squashes={self.squashes}")
        return f"Checks({', '.join(args)})"


    def __repr__(self):
        return self.__str__()


    def validate(self, commit: Commit) -> bool:
        check_result = CheckResult(commit)
        if not isinstance(commit, Commit):
            raise TypeError("Checks.validate requires a Commit object")

        if self.branches:
            for branch in self.branches:
                branch_present = branch in commit.branches
                check_result.add_branch(branch, branch_present)

        if self.tags:
            for tag in self.tags:
                tag_present = tag in commit.tags
                check_result.add_tag(tag, tag_present)

        if self.cherry_pick:
            check_result.cherry_pick = self.cherry_pick
            check_result.is_cherry_picked = commit.is_cherry_picked_from(self.cherry_pick)

        if self.reverts:
            check_result.reverts = self.reverts
            check_result.is_reverted = commit.reverts(self.reverts)

        if self.squashes:
            check_result.squashes = self.squashes
            check_result.is_squashed = commit.squashes(self.squashes)

        return check_result
