class Commit:
    def __init__(self, id):
        self.id = id
        self.hash = ""
        self.message = ""
        self.committed_date = None
        self.diff = None

        self.branches = []
        self.tags = []
        self.parents = []

        self.is_cherry_picked = False
        self.cherry_picked_from = None

        self.reverts = False
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
            args.append(f"tags={self.tags}")
        if self.parents:
            args.append(f"parents={self.parents}")
        return f"Commit({', '.join(args)})"


    def __repr__(self):
        return self.__str__()


    def is_cherry_picked_from(self, commit):
        self.is_cherry_picked = self.message == commit.message \
            and self.diff == commit.diff
        self.cherry_picked_from = commit
        return self.is_cherry_picked

    def revert(self, commit):
        self.reverts = False
        self.reverting_commit = commit
        return False
