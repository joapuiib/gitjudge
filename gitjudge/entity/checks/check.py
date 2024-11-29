from gitjudge.entity import Commit

class Check:
    def __init__(self):
        self.tags = []
        self.branches = []
        self.cherry_pick = None
        self.reverts = None
        self.squashes = None
        self.diff = None
        self.file_content = None


    def __str__(self):
        return f"Check()"


    def __repr__(self):
        return self.__str__()


    def resolve_references(self, resolver):
        pass


    def validate(self, commit: Commit) -> bool:
        return True
