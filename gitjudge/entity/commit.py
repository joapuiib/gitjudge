import re

class Commit:
    def __init__(self, id):
        self.id = id
        self.hash = ""
        self.message = ""
        self.committed_date = None
        self._diff = None

        self.branches = []
        self.tags = []
        self.parents = []

        self.is_cherry_picked = False
        self.cherry_picked_from = None

        self.is_reverted = False
        self.reverting_commit = None


    def short_hash(self):
        return self.hash[:7]


    def short_message(self):
        return self.message.split("\n")[0]

    def __str__(self):
        args = []
        args.append(f"id={self.id}")
        if self.hash:
            args.append(f"hash={self.hash}")
        if self.message:
            args.append(f"message={self.message}")
        if self.branches:
            args.append(f"branches={self.branches}")
        if self.tags:
            args.append(f"tas={self.tags}")
        if self.parents:
            args.append(f"parents={self.parents}")
        return f"Commit({', '.join(args)})"


    def __repr__(self):
        return self.__str__()


    def is_cherry_picked_from(self, commit):
        self.is_cherry_picked = self.message == commit.message \
            and self.diff() == commit.diff()
        self.cherry_picked_from = commit
        return self.is_cherry_picked

    def show_diff(self, colored=True):
        print(self.diff(colored=colored))

    def diff(self, colored=False):
        if not colored:
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            return ansi_escape.sub('', self._diff)
        return self._diff

    def reverts(self, commit):
        self_diff_lines = set(self.diff().splitlines())
        commit_diff_lines = set(commit.diff().splitlines())

        expected_revert_lines = { \
                    "-" + line[1:] if line.startswith("+") \
                else \
                    "+" + line[1:] \
                for line in self_diff_lines \
                if line.startswith(("+", "-")) \
        }

        self.is_reverted = expected_revert_lines <= commit_diff_lines
        self.reverting_commit = commit

        return self.is_reverted

