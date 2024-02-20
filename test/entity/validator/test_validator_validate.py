import pytest
from gitjudge.entity import Validator

"""
* f11d9bd - (0 seconds ago) 3. added branch1.md - Joan Puigcerver (branch1)
* de3c9f4 - (0 seconds ago) 2. modified file1.md - Joan Puigcerver (HEAD -> main)
* 24fd9a6 - (0 seconds ago) 1. added file1.md - Joan Puigcerver
Definition(
    name=test-definition,
    expected_commits=[
        ExpectedCommit(id=1, message=1.),
        ExpectedCommit(id=2, message=2.),
        ExpectedCommit(id=3, message=3., start=branch1)
    ]
)
"""

@pytest.fixture
def validator(repo, definition):
    return Validator(repo, definition)

def test_validateShouldExist(validator):
    assert hasattr(validator, "validate")

def test_givenWithWrongType_shouldRaiseError(validator):
    validator.validate()
    assert len(validator.found_commits) == 3
    assert validator.found_commits["1"].message == "1. added file1.md"
    assert validator.found_commits["2"].message == "2. modified file1.md"
    assert validator.found_commits["3"].message == "3. added branch1.md"
