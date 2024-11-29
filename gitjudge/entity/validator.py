import re
from colorama import Fore, Style

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
        for cd in self.definition.commits:
            cd.resolve_references(self.resolver)
            commit = self.repo.find_commit(cd)

            # If commit is found, validate it
            if isinstance(commit, NotFoundCommit):
                print(f"==== {Fore.RED}Commit {cd.id} not found in repository{Fore.RESET}")
                self.formatter.print_commit_definition(cd)
            else:
                cd.validate(commit, self.repo)
                self.formatter.print_commit(self.definition, cd, commit)
