import pytest
from gitjudge.entity import CheckResult, Commit, CherryPickState

def test_defaultCheckResult_shouldReturnFalse():
    commit = Commit(1)
    check_result = CheckResult(commit)
    assert check_result.checked_cherry_status == CherryPickState.NO_CHERRYPICK_CHECK
    assert not check_result.has_checked_cherry_pick()
    assert not check_result.has_found_cherry_pick_commit()
    assert check_result.is_correct()

def test_checkResultCheckedNotFoundCommit():
     commit = Commit(1)
     check_result = CheckResult(commit)
     check_result.set_cherry_picked(None, False)
     assert check_result.checked_cherry_status == CherryPickState.CHERRYPICK_COMMIT_NOT_FOUND
     assert check_result.has_checked_cherry_pick()
     assert not check_result.has_found_cherry_pick_commit()
     assert not check_result.is_cherry_picked()

def test_checkResultCheckedButNotCherryPicked():
    commit = Commit(1)
    commit2 = Commit(2)
    check_result = CheckResult(commit)
    check_result.set_cherry_picked(commit2, False)
    assert check_result.checked_cherry_status == CherryPickState.NO_CHERRYPICKED
    assert check_result.has_checked_cherry_pick()
    assert check_result.has_found_cherry_pick_commit()
    assert not check_result.is_cherry_picked()
    assert not check_result.is_correct()

def test_checkResultCheckedAndCherryPicked():
    commit = Commit(1)
    commit2 = Commit(2)
    check_result = CheckResult(commit)
    check_result.set_cherry_picked(commit2, True)
    assert check_result.checked_cherry_status == CherryPickState.CHERRYPICKED
    assert check_result.has_found_cherry_pick_commit()
    assert check_result.has_checked_cherry_pick()
    assert check_result.is_cherry_picked()
    assert check_result.is_correct()
