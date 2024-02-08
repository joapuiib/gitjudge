import pytest

from gitjudge.entity import Checks, Commit

@pytest.fixture
def found_commits():
    return {
        1: Commit(
            1,
            message="Commit 1",
            tags=["tag1"],
            diff="+1"
        ),
        2: Commit(
            2,
            message="Commit 2",
            tags=["tag2"],
            diff="+2"
        ),
        3: Commit(
            3,
            message="Revert \"Commit 2\"",
            diff="-2"
        ),
        4: Commit(
            4,
            message="Cherry-pick \"Commit 1\"",
            diff="+1"
        ),
    }

def test_chekcsValidate_WrongParameters_ShouldRaiseError():
    checks = Checks()
    with pytest.raises(TypeError):
        checks.validate("not a commit")


def test_checksValidate_NoTagChecks_ShouldReturnNoTags(found_commits):
    checks = Checks()
    commit = found_commits[1]
    check_result = checks.validate(commit, found_commits)
    assert check_result.tags == {}


def test_checksValidate_NotSameTagChecks_ShouldReturnNoFoundTag(found_commits):
    checks = Checks()
    checks.tags = ["tag2"]
    commit = found_commits[1]
    check_result = checks.validate(commit, found_commits)
    assert check_result.tags == {"tag2": False}

def test_checksValidate_SameTagChecks_ShouldReturnFoundTag(found_commits):
    checks = Checks()
    checks.tags = ["tag1"]
    commit = found_commits[1]
    check_result = checks.validate(commit, found_commits)
    assert check_result.tags == {"tag1": True}

def test_checksValidate_NoCherryPickChecks_ShouldReturnNoCherryPick(found_commits):
    checks = Checks()
    commit = found_commits[1]
    check_result = checks.validate(commit, found_commits)
    assert not check_result.has_checked_cherry_pick()

def test_checksValidate_CherryPickChecks_ShouldReturnCherryPick(found_commits):
    checks = Checks()
    checks.cherry_pick = 1
    commit = found_commits[4]
    check_result = checks.validate(commit, found_commits)
    assert check_result.has_checked_cherry_pick()
    assert check_result.has_found_cherry_pick_commit()
    assert check_result.is_cherry_picked()

def test_checksValidate_CherryPickChecks_ShouldReturnNotCherryPick(found_commits):
    checks = Checks()
    checks.cherry_pick = 2
    commit = found_commits[4]
    check_result = checks.validate(commit, found_commits)
    assert check_result.has_checked_cherry_pick()
    assert check_result.has_found_cherry_pick_commit()
    assert not check_result.is_cherry_picked()

def test_checksValidate_CherryPickChecks_ShouldReturnNotCherryPickWhenNotFound(found_commits):
    checks = Checks()
    checks.cherry_pick = 1
    commit = found_commits[4]
    check_result = checks.validate(commit, {})
    print(check_result)
    assert check_result.has_checked_cherry_pick()
    assert not check_result.has_found_cherry_pick_commit()
    assert not check_result.is_cherry_picked()
