class LogOptions:
    def __init__(self):
        self.branches = None
        self.all = False

    def __str__(self):
        args = []
        if self.branches is not None:
            args.append(f"branches={self.branches}")
        if self.all:
            args.append("all=True")
        return f"LogOptions({', '.join(args)})"

    def __repr__(self):
        return self.__str__()
