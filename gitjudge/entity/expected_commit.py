class ExpectedCommit:
    def __init__(self, id):
        self.id = id
        self.message = None
        self.starting_point = None

        self.parents = []
        self.branches = []
        self.tags = []

    def set_message(self, message):
        self.message = message

    def add_branch(self, branch):
        self.branches.append(branch)

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_parent(self, parent):
        self.parents.append(parent)

