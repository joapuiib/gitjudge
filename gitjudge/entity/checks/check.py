class Check:
    def __init__(self):
        self.checked = False
        self.correct = False


    def __str__(self):
        return f"Check()"


    def __repr__(self):
        return self.__str__()


    def resolve_references(self, commit_id, resolver):
        pass


    def validate(self, commit, repo) -> bool:
        self.checked = True
        self.correct = True
        return self.correct
