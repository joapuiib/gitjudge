import pytest
from gitjudge.entity import CheckResult, Commit

def test_givenConstructorWithoutCommit_shouldRaiseError():
    with pytest.raises(TypeError):
        CheckResult()

def test_checkResultConstructorWithWrongType_shouldRaiseError():
    with pytest.raises(TypeError):
        CheckResult("str")

def test_checkResultConstructorWithCommit_shouldHaveDefaultValues():
    commit = Commit(1)
    check_result = CheckResult(commit)
    assert check_result.commit == commit
    assert check_result.tags == {}
    assert check_result.cherry_picked == (None, False)
    assert check_result.checked_cherry_pick == False
    # assert check_result.reverted == (None, False)
