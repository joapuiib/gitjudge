import re

from gitjudge.entity import Definition, Repository, Commit, NotFoundCommit, ReferencedItselfCommit
from gitjudge.formatter.stdout import print_commit, print_expected_commit

from colorama import Fore, Style

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
            self.resolve_references_expected_commit(expected_commit)
            # print(expected_commit)
            print(f"{Fore.CYAN}Validating commit {expected_commit.id}{Fore.RESET}")
            commit = self.repo.find_commit(expected_commit)
            if isinstance(commit, NotFoundCommit):
                print(f"{Fore.RED}Commit {expected_commit.id} not found in repository{Fore.RESET}")
                print_expected_commit(expected_commit)
                print()
                continue

            self.resolve_references_checks(expected_commit, commit)
            self.found_commits[expected_commit.id] = commit
            check_result = expected_commit.validate(commit)
            print_commit(commit, check_result)

            print()

        min_id = min(self.found_commits.keys())
        first_commit = self.found_commits[min_id]
        max_id = max(self.found_commits.keys())
        last_commit = self.found_commits[max_id]

        print("# Repository log:")
        self.repo.print_log(
            start=first_commit,
            end=last_commit,
            branches=self.definition.log_options.branches,
            all=self.definition.log_options.all
        )



    def _resolve_reference(self, id, reference):
        if reference and re.match(r"-?\d+", str(reference)):
            if reference in self.found_commits:
                if reference == id:
                    return ReferencedItselfCommit(id)
                else:
                    return self.found_commits[reference]
            else:
                return NotFoundCommit(id)
                # raise ValueError(f"{commit_ref.capitalize()} {ref_attr} not found in commits")
        else:
            commit = self.repo.find_commit_by_ref(reference)
            return commit


    def resolve_references_expected_commit(self, expected_commit):
        id = expected_commit.id
        if expected_commit.start:
            expected_commit.start = self._resolve_reference(id, expected_commit.start)

        if expected_commit.end:
            expected_commit.end = self._resolve_reference(id, expected_commit.end)


    def resolve_references_checks(self, expected_commit, commit=None):
        id = expected_commit.id
        checks = expected_commit.checks
        if checks:
            if checks.cherry_pick:
                checks.cherry_pick = self._resolve_reference(id, checks.cherry_pick)

            if checks.reverts:
                checks.reverts = self._resolve_reference(id, checks.reverts)

            if checks.squashes:
                if isinstance(checks.squashes, list):
                    for i, reference in enumerate(checks.squashes):
                        checks.squashes[i] = self._resolve_reference(id, reference)

                else:
                    if not commit:
                        raise ValueError("Expected commit required to resolve squashes")
                    checks.squashes = self.repo.find_commits_in_branch(checks.squashes, commit)
