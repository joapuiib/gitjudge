from gitjudge.entity import Checks
from gitjudge.entity import DiffList, DiffIndex

def map_checks(d: dict) -> Checks:
    if not isinstance(d, dict):
        raise TypeError('Expected dict object')

    checks = Checks()

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

    checks.branches = branches

    # Parent and parents are mutually exclusive
    if 'parent' in d and 'parents' in d:
        raise ValueError('Expected commit cannot have both parent and parents')

    parents = d.get('parents', [])
    parent = d.get('parent')
    if parent:
        parents.append(parent)
    checks.parents = parents

    if len(parents) > 2:
        raise ValueError('Expected commit cannot have more than 2 parents')

    # Tag and tags are mutually exclusive
    if 'tag' in d and 'tags' in d:
        raise ValueError('Expected commit cannot have both tag and tags')

    tags = d.get('tags', [])
    tag = d.get('tag')
    if tag:
        tags.append(tag)
    checks.tags = tags

    checks.cherry_pick = d.get('cherry-pick', None) or d.get('cherry-picks', None)
    checks.reverts = d.get('reverts', None)
    checks.squashes = d.get('squashes', None)

    config_diff = d.get('diff', None)
    if config_diff:
        checks.diff = DiffList()
        for file, text in config_diff.items():
            diffindex = DiffIndex(file)
            for line in text.split('\n'):
                if line.startswith('+'):
                    diffindex.add_addition(line[1:])
                elif line.startswith('-'):
                    diffindex.add_deletion(line[1:])
            checks.diff.add(diffindex)

    return checks
