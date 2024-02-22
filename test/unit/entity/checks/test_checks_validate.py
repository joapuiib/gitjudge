import pytest

from gitjudge.entity import Checks, Commit

def test_chekcsValidate_WrongParameters_ShouldRaiseError():
    checks = Checks()
    with pytest.raises(TypeError):
        checks.validate("not a commit")


def test_checksValidate_NoTagChecks_ShouldReturnNoTags(found_commits):
    checks = Checks()
    commit = found_commits[1]
    check_result = checks.validate(commit)
    assert check_result.tags == {}


def test_checksValidate_NotSameTagChecks_ShouldReturnNoFoundTag(found_commits):
    checks = Checks()
    checks.tags = ["T2"]
    commit = found_commits[1]
    check_result = checks.validate(commit)
    assert check_result.tags == {"T2": False}

def test_checksValidate_SameTagChecks_ShouldReturnFoundTag(found_commits):
    checks = Checks()
    checks.tags = ["T1"]
    commit = found_commits[1]
    check_result = checks.validate(commit)
    assert check_result.tags == {"T1": True}

def test_checksValidate_NoCherryPickChecks_ShouldReturnNoCherryPick(found_commits):
    checks = Checks()
    commit = found_commits[1]
    check_result = checks.validate(commit)
    assert not check_result.has_checked_cherry_pick()

def test_checksValidate_CherryPickChecks_ShouldReturnCherryPick(found_commits):
    checks = Checks()
    checks.cherry_pick = found_commits[1]
    commit = found_commits[4]
    check_result = checks.validate(commit)
    assert check_result.has_checked_cherry_pick()
    assert check_result.has_found_cherry_pick_commit()
    assert check_result.is_cherry_picked()

def test_checksValidate_CherryPickChecks_ShouldReturnNotCherryPick(found_commits):
    checks = Checks()
    checks.cherry_pick = found_commits[2]
    commit = found_commits[4]
    check_result = checks.validate(commit)
    assert check_result.has_checked_cherry_pick()
    assert check_result.has_found_cherry_pick_commit()
    assert not check_result.is_cherry_picked()
