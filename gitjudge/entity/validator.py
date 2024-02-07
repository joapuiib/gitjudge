from gitjudge.entity import Definition, Repository

class Validator:
    def __init__(self, repo, definition):
        if not isinstance(repo, Repository):
            raise ValueError(f"Expected Repository, got {type(repo)}")
        self.repo = repo

        if not isinstance(definition, Definition):
            raise TypeError(f"Expected Definition, got {type(definition)}")
        self.definition = definition
        self.found_commits = {}

    def validate(self):
        for expected_commit in self.definition.expected_commits:
            # TODO show on verbose: print(f"Validating commit {expected_commit}")
            commit = self.repo.find_commit(expected_commit)
            self.found_commits[expected_commit.id] = commit
