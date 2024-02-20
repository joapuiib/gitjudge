import pytest
from gitjudge.entity import CheckResult, Commit, RevertState

def test_defaultCheckResult_shouldReturnFalse():
    commit = Commit(1)
    check_result = CheckResult(commit)
    assert check_result.checked_revert_status == RevertState.NO_REVERT_CHECK
    assert not check_result.has_checked_revert()
    assert not check_result.has_found_reverted_commit()
    assert check_result.is_correct()

def test_checkResultCheckedNotFoundCommit():
    commit = Commit(1)
    check_result = CheckResult(commit)
    check_result.set_reverted(None, False)
    assert check_result.checked_revert_status == RevertState.REVERT_COMMIT_NOT_FOUND
    assert check_result.has_checked_revert()
    assert not check_result.has_found_reverted_commit()
    assert not check_result.is_reverted()

def test_checkResultCheckedButNotReverted():
    commit = Commit(1)
    commit2 = Commit(2)
    check_result = CheckResult(commit)
    check_result.set_reverted(commit2, False)
    assert check_result.checked_revert_status == RevertState.NO_REVERTED
    assert check_result.has_checked_revert()
    assert not check_result.is_reverted()
    assert not check_result.is_correct()

def test_checkResultCheckedAndReverted():
    commit = Commit(1)
    commit2 = Commit(2)
    check_result = CheckResult(commit)
    check_result.set_reverted(commit2, True)
    assert check_result.checked_revert_status == RevertState.REVERTED
    assert check_result.has_checked_revert()
    assert check_result.is_reverted()
    assert check_result.is_correct()
