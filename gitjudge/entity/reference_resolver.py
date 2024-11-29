import re

from gitjudge.entity import Definition, Repository, Commit, NotFoundCommit, ReferencedItselfCommit
from gitjudge.formatter import Formatter


class ReferenceResolver:
    def __init__(self):
        self.references = {}

    def resolve_reference(self, reference):
        if reference in self.found_commits:
            if reference == id:
                return ReferencedItselfCommit()
            else:
                return self.found_commits[reference]
        else:
            return NotFoundCommit()
            # raise ValueError(f"{commit_ref.capitalize()} {ref_attr} not found in commits")
