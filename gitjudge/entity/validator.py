import re

from gitjudge.entity import Definition, Repository, Commit, NotFoundCommit, ReferencedItselfCommit, ReferenceResolver
from gitjudge.formatter import Formatter


class Validator:
    def __init__(self, args, definition: Definition, repo: Repository, formatter: Formatter):
        self.args = args
        self.definition = definition
        self.repo = repo
        self.formatter = formatter

        self.resolver = ReferenceResolver(repo)


    def validate(self):
        for commit_definition in self.definition.commits:
            print(commit_definition)
            commit_definition.resolve_references(self.resolver)
            commit = self._find_commit(commit_definition)
            print(commit)

            # If commit is found, validate it
            if commit:
                commit_definition.validate(commit, self.repo)


    def _find_commit(self, commit_definition) -> Commit:
        commit = self.repo.find_commit(commit_definition)
        if commit:
            return commit
