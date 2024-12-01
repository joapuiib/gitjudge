from gitjudge.entity.checks import SquashCheck


def map_squash_check(d: dict) -> list:
    if not isinstance(d, dict):
        raise TypeError("Expected dict object")

    checks = []

    squashes = d.get("squashes", None)
    if squashes:
        checks.append(SquashCheck(squashes))

    return checks
