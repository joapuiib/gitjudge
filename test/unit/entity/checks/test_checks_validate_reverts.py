import pytest

from gitjudge.entity import Checks, Commit, NotFoundCommit, ReferencedItselfCommit

def test_checksValidate_NoRevertChecks_ShouldReturnNoRevert(found_commits):
    checks = Checks()
    commit = found_commits[1]
    check_result = checks.validate(commit)
    assert check_result.reverts == None
    assert not check_result.is_reverted

def test_checksValidate_RevertChecks_ShouldReturnReverts(found_commits):
    # Commit 3 is a revert of commit 2
    checks = Checks()
    checks.reverts = found_commits[2]
    commit = found_commits[3]
    check_result = checks.validate(commit)
    assert check_result.reverts == found_commits[2]
    assert check_result.is_reverted

def test_checksValidate_RevertChecks_ShouldReturnNotReverts(found_commits):
    # Commit 3 is not a revert of commit 1
    checks = Checks()
    checks.reverts = found_commits[1]
    commit = found_commits[3]
    check_result = checks.validate(commit)
    assert check_result.reverts == found_commits[1]
    assert not check_result.is_reverted


def test_checksValidate_RevertNotFoundCommit_ShouldReturnNotRevert(found_commits):
    checks = Checks()
    checks.reverts = NotFoundCommit(1)
    commit = found_commits[3]
    check_result = checks.validate(commit)
    assert isinstance(check_result.reverts, NotFoundCommit)
    assert not check_result.is_reverted

def test_checksValidate_RevertReferencedItselfCommit_ShouldReturnNotRevert(found_commits):
    checks = Checks()
    checks.reverts = ReferencedItselfCommit(1)
    commit = found_commits[3]
    check_result = checks.validate(commit)
    assert isinstance(check_result.reverts, ReferencedItselfCommit)
    assert not check_result.is_reverted
