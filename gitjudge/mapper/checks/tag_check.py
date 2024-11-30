from gitjudge.entity.checks import TagCheck


def map_tag_check(d: dict) -> list:
    if not isinstance(d, dict):
        raise TypeError('Expected dict object')

    checks = []

    # Tag and tags are mutually exclusive
    if 'tag' in d and 'tags' in d:
        raise ValueError('Commit difinition checks cannot have both tag and tags optionS')

    tags = d.get('tags', [])
    tag = d.get('tag')
    if tag:
        tags.append(tag)

    if tags:
        checks.append(TagCheck(tags))

    return checks
