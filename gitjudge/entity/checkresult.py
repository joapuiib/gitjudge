from gitjudge.entity import Commit

class CheckResult:
    def __init__(self, commit):
        self.commit = commit
        if not isinstance(commit, Commit):
            raise TypeError("CheckResult must be initialized with a Commit object.")

        self.tags = {}

        """
        cherry_picked[0] is the commit that was cherry-picked from.
        cherry_picked[1] is a boolean indicating if the commit was cherry-picked.
        """
        self.cherry_picked = (None, False)
        self.checked_cherry_pick = False

        """
        reverted[0] is the commit that was reverted.
        reverted[1] is a boolean indicating if the commit was reverted.
        """
        self.reverted = (None, False)

    def set_cherry_picked(self, commit, is_cherry_picked):
        self.checked_cherry_pick = True
        if commit:
            self.cherry_picked = (commit, is_cherry_picked)

    def has_checked_cherry_pick(self):
        return self.checked_cherry_pick

    def is_cherry_picked(self):
        return self.cherry_picked[1]

