import re

from gitjudge.entity import Definition, Repository, Commit, NotFoundCommit, ReferencedItselfCommit
from gitjudge.formatter import Formatter


class ReferenceResolver:
    def __init__(self, repo: Repository):
        self.references = {}
        self.repo = repo

    def resolve_reference(self, commit_id, reference):
        if reference and re.match(r"-?\d+", str(reference)):
            if reference in self.references:
                if reference == commit_id:
                    return ReferencedItselfCommit(commit_id)
                else:
                    return self.references[reference]
            else:
                return NotFoundCommit(commit_id)
                # raise ValueError(f"{commit_ref.capitalize()} {ref_attr} not found in commits")

        else:
            # TODO: Repensar resolve references from repo
            commit = self.repo.find_commit_by_ref(reference)
            return commit

