import pytest
from gitjudge.entity import CheckResult, Commit

def test_defaultCheckResult_shouldReturnFalse():
    commit = Commit(1)
    check_result = CheckResult(commit)
    assert not check_result.has_checked_cherry_pick()

def test_checkResultCheckedButNotCherryPicked():
    commit = Commit(1)
    commit2 = Commit(2)
    check_result = CheckResult(commit)
    check_result.set_cherry_picked(commit2, True)
    assert check_result.has_checked_cherry_pick()
    assert check_result.is_cherry_picked()

def test_checkResultCheckedAndCherryPicked():
    commit = Commit(1)
    commit2 = Commit(2)
    check_result = CheckResult(commit)
    check_result.set_cherry_picked(commit2, False)
    assert check_result.has_checked_cherry_pick()
    assert not check_result.is_cherry_picked()
