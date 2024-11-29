from gitjudge.entity.checks import *
from gitjudge.entity import DiffList, DiffIndex

def map_checks(d: dict) -> Check:
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

    # checks.add(BranchCheck(branches))

    # Parent and parents are mutually exclusive
    if 'parent' in d and 'parents' in d:
        raise ValueError('Expected commit cannot have both parent and parents')

    parents = d.get('parents', [])
    parent = d.get('parent')
    if parent:
        parents.append(parent)
    # checks.add(ParentCheck(parents))

    if len(parents) > 2:
        raise ValueError('Expected commit cannot have more than 2 parents')

    # Tag and tags are mutually exclusive
    if 'tag' in d and 'tags' in d:
        raise ValueError('Expected commit cannot have both tag and tags')

    tags = d.get('tags', [])
    tag = d.get('tag')
    if tag:
        tags.append(tag)
    checks.add(TagCheck(tags))

    cherry_pick = d.get('cherry-pick', None) or d.get('cherry-picks', None)
    if cherry_pick:
        # checks.add(CherryPickCheck(cherry_pick))
        pass

    checks.reverts = d.get('reverts', None)
    if checks.reverts:
        # checks.add(RevertCheck(checks.reverts))
        pass
    checks.squashes = d.get('squashes', None)
    if checks.squashes:
        # checks.add(SquashCheck(checks.squashes))
        pass

    """
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

    checks.file_content = d.get('file-content', None)
    """

    return checks
