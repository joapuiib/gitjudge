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
            self.resolve_references(expected_commit)
            # print(expected_commit)
            print(f"{Fore.CYAN}Validating commit {expected_commit.id}{Fore.RESET}")
            commit = self.repo.find_commit(expected_commit)
            if isinstance(commit, NotFoundCommit):
                print(f"{Fore.RED}Commit {expected_commit.id} not found in repository{Fore.RESET}")
                print_expected_commit(expected_commit)
                print()
                continue

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

    def _resolve_reference(self, id, obj, reference):
        ref_attr = getattr(obj, reference)
        if ref_attr and re.match(r"-?\d+", str(ref_attr)):
            if ref_attr in self.found_commits:
                if ref_attr == id:
                    setattr(obj, reference, ReferencedItselfCommit(id))
                else:
                    setattr(obj, reference, self.found_commits[ref_attr])
            else:
                setattr(obj, reference, NotFoundCommit(id))
                # raise ValueError(f"{commit_ref.capitalize()} {ref_attr} not found in commits")
        else:
            commit = self.repo.find_commit_by_ref(ref_attr)
            setattr(obj, reference, commit)

    def resolve_references(self, expected_commit):
        id = expected_commit.id
        if expected_commit.start:
            self._resolve_reference(id, expected_commit, "start")

        if expected_commit.end:
            self._resolve_reference(id, expected_commit, "end")

        checks = expected_commit.checks
        if checks:
            if checks.cherry_pick:
                self._resolve_reference(id, checks, "cherry_pick")

            if checks.reverts:
                self._resolve_reference(id, checks, "reverts")
