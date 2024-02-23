import pytest

from gitjudge.entity import Checks, Commit, NotFoundCommit, ReferencedItselfCommit

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
    assert check_result.cherry_pick == None
    assert not check_result.is_cherry_picked

def test_checksValidate_CherryPickChecks_ShouldReturnCherryPick(found_commits):
    # Commit 4 is a cherry-pick of Commit 1
    checks = Checks()
    checks.cherry_pick = found_commits[1]
    commit = found_commits[4]
    check_result = checks.validate(commit)
    assert check_result.cherry_pick == found_commits[1]
    assert check_result.is_cherry_picked

def test_checksValidate_CherryPickChecks_ShouldReturnNotCherryPick(found_commits):
    # Commit 4 is not a cherry-pick of commit 2
    checks = Checks()
    checks.cherry_pick = found_commits[2]
    commit = found_commits[4]
    check_result = checks.validate(commit)
    assert check_result.cherry_pick == found_commits[2]
    assert not check_result.is_cherry_picked

def test_checksValidate_CherryPickNotFoundCommit_ShouldReturnNotCherryPick(found_commits):
    checks = Checks()
    checks.cherry_pick = NotFoundCommit(1)
    commit = found_commits[4]
    check_result = checks.validate(commit)
    assert isinstance(check_result.cherry_pick, NotFoundCommit)
    assert not check_result.is_cherry_picked

def test_checksValidate_CherryPickReferencedItselfCommit_ShouldReturnNotCherryPick(found_commits):
    checks = Checks()
    checks.cherry_pick = ReferencedItselfCommit(1)
    commit = found_commits[4]
    check_result = checks.validate(commit)
    assert isinstance(check_result.cherry_pick, ReferencedItselfCommit)
    assert not check_result.is_cherry_picked


