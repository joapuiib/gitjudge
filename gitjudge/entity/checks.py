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
