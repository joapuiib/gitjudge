class CommitDefinition:
    def __init__(self, id: str, message: str = None, start: str = None, end: str = None):
        self.id = id
        self.message = message
        self.start = start
        self.end = end

        self.branches = []
        self.tags = []

        self.show = False
        self.checks = []

        self.is_correct = False


    def set_message(self, message):
        self.message = message


    def add_branch(self, branch):
        self.branches.append(branch)


    def add_tag(self, tag):
        self.tags.append(tag)


    def add_check(self, check):
        self.checks.append(check)


    def __str__(self):
        args = []
        args.append(f"id={self.id}")
        if self.message:
            args.append(f"message={self.message}")
        if self.start:
            args.append(f"start={self.start}")
        if self.end:
            args.append(f"end={self.end}")
        if self.checks:
            args.append(f"checks={self.checks}")
        return f"CommitDefinition({', '.join(args)})"


    def __repr__(self):
        return self.__str__()


    def resolve_references(self, resolver):
        if self.start:
            self.start = resolver.resolve_reference(self.id, self.start)
            self.start.id = self.id
        if self.end:
            self.end = resolver.resolve_reference(self.id, self.end)
            self.end.id = self.id

        for check in self.checks:
            check.resolve_references(self.id, resolver)


    def validate(self, commit, repo):
        self.is_correct = True
        for check in self.checks:
            check_correct = check.validate(commit, repo)
            self.is_correct = self.is_correct and check_correct
