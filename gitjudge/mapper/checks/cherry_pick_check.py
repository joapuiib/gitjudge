from gitjudge.entity.checks import CherryPickCheck


def map_cherry_pick_check(d: dict) -> list:
    if not isinstance(d, dict):
        raise TypeError('Expected dict object')

    checks = []

    cherry_pick = d.get('cherry-pick', None) or d.get('cherry-picks', None)
    if cherry_pick:
        checks.append(CherryPickCheck(cherry_pick))

    return checks
