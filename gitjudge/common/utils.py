import re

def resolve_commit_reference(obj, id, commit_ref, found_commits):
    ref_attr = getattr(obj, commit_ref)
    if ref_attr and re.match(r"-?\d+", str(ref_attr)):
        if ref_attr in found_commits:
            if ref_attr == id:
                raise ValueError(f"{commit_ref.capitalize()} cannot reference itself")
            setattr(obj, commit_ref, found_commits[ref_attr])
        else:
            raise ValueError(f"{commit_ref.capitalize()} {ref_attr} not found in commits")


