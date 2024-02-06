from gitjudge.entity.expected_commit import ExpectedCommit

def map_expected_commit(d: dict) -> ExpectedCommit:
    id = d.get('id')
    if not id:
        raise ValueError('Expected commit id is required')
    expected_commit = ExpectedCommit(id)

    expected_commit.message = d.get('message')
    expected_commit.starting_point = d.get('starting_point')

    # Parent and parents are mutually exclusive
    if 'parent' in d and 'parents' in d:
        raise ValueError('Expected commit cannot have both parent and parents')

    parents = d.get('parents', [])
    parent = d.get('parent')
    if parent:
        parents.append(parent)
    expected_commit.parents = parents

    if len(parents) > 2:
        raise ValueError('Expected commit cannot have more than 2 parents')

    # Tag and tags are mutually exclusive
    if 'tag' in d and 'tags' in d:
        raise ValueError('Expected commit cannot have both tag and tags')

    tags = d.get('tags', [])
    tag = d.get('tag')
    if tag:
        tags.append(tag)
    expected_commit.tags = tags

    return expected_commit
