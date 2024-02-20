from gitjudge.entity import ExpectedCommit
from gitjudge.mapper import map_checks

def map_expected_commit(id: str, d: dict) -> ExpectedCommit:
    if not isinstance(d, dict):
        raise TypeError('Expected dict object')

    expected_commit = ExpectedCommit(id)

    if 'message' in d:
        expected_commit.message = d.get('message')
        if not expected_commit.message:
            raise ValueError('Expected commit message cannot be empty')

    expected_commit.start = d.get('start')
    expected_commit.end = d.get('end')

    checks = d.get('check', None)
    if checks:
        expected_commit.checks = map_checks(checks)

    return expected_commit
