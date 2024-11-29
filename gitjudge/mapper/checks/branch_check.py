from gitjudge.entity.checks import *
from gitjudge.entity.checks import TagCheck

def map_branch_check(d: dict) -> list:
    if not isinstance(d, dict):
        raise TypeError('Expected dict object')

    checks = []

    # Branch and branches are mutually exclusive
    if 'branch' in d and 'branches' in d:
        raise ValueError('Expected commit cannot have both branch and branches')

    branches = d.get('branches', [])
    if branches is not None and not isinstance(branches, list):
        branches = [branches]

    branch = d.get('branch', [])
    if branch is not None and not isinstance(branch, list):
        branch = [branch]

    if branch:
        branches += branch

    if branches:
        checks.append(BranchCheck(branches))

    return checks
