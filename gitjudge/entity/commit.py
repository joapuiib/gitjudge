class Commit:
    def __init__(self, id):
        self.id = id
        self.hash = ""
        self.message = ""

        self.branches = []
        self.tags = []
        self.parents = []

    def set_hash(self, hash):
        self.hash = hash

    def set_message(self, message):
        self.message = message

    def add_branch(self, branch):
        self.branches.append(branch)

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_parent(self, parent):
        self.parents.append(parent)

