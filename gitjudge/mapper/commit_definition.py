from gitjudge.entity.commit_definition import CommitDefinition
from gitjudge.mapper.checks.checks import map_checks


def map_commit_definition(id: str, d: dict) -> CommitDefinition:
    if not isinstance(d, dict):
        raise TypeError("Expected dict object")

    cd = CommitDefinition(id)

    cd.ref = d.get("ref")
    cd.message = d.get("message")
    cd.start = d.get("start")
    cd.end = d.get("end")
    cd.show = d.get("show", False)

    checks = d.get("check", [])
    if checks:
        cd.checks = map_checks(checks)

    return cd
