from gitjudge.entity.checks import RevertsCheck


def map_reverts_check(d: dict) -> list:
    if not isinstance(d, dict):
        raise TypeError('Expected dict object')

    checks = []

    reverts = d.get('reverts', None)
    if reverts:
        checks.append(RevertsCheck(reverts))

    return checks
