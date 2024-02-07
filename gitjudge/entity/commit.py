class Commit:
    def __init__(self, id):
        self.id = id
        self.hash = ""
        self.message = ""
        self.committed_date = None

        self.branches = []
        self.tags = []
        self.parents = []

    def short_hash(self):
        return self.hash[:7]

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
