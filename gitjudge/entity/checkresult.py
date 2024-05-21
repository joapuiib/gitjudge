from gitjudge.entity import Commit

class CheckResult:
    def __init__(self, commit):
        self.commit = commit
        if not isinstance(commit, Commit):
            raise TypeError("CheckResult must be initialized with a Commit object.")

        self.tags = {}
        self.branches = {}

        self.cherry_pick = None
        self.is_cherry_picked = False

        self.reverts = None
        self.is_reverted = False

        self.squashes = None
        self.is_squashed = False

    def __str__(self):
        args = []
        args.append(f"commit={self.commit}")
        if self.branches:
            args.append(f"branches={self.branches}")
        if self.tags:
            args.append(f"tags={self.tags}")
        if self.cherry_pick:
            args.append(f"cherry_pick={self.cherry_pick}, is_cherry_picked={self.is_cherry_picked}")
        if self.reverts:
            args.append(f"reverts={self.reverts}, is_reverted={self.is_reverted}")
        if self.squashes:
            args.append(f"squashes={self.squashes}, is_squashed={self.is_squashed}")
        return f"CheckResult({', '.join(args)})"

    def __repr__(self):
        return self.__str__()

    def is_correct(self):
        correct = True
        # Check if all tags are present
        if self.tags:
            correct = correct and all(self.tags.values())
        if self.cherry_pick:
            correct = correct and self.is_cherry_picked
        if self.reverts:
            correct = correct and self.is_reverted
        if self.squashes:
            correct = correct and self.is_squashed
        return correct


    def add_tag(self, tag, present):
        self.tags[tag] = present
        return self

    def add_branch(self, branch, present):
        self.branches[branch] = present
        return self
