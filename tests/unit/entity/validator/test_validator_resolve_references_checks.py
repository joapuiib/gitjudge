import pytest

from gitjudge.entity import Validator, Checks, ExpectedCommit, Commit, NotFoundCommit, ReferencedItselfCommit

def testResolveReferences_givenNothing_expectNoChange(validator):
    expected = ExpectedCommit("id")
    validator.resolve_references_checks(expected)

    assert expected.start == None
    assert expected.end == None
    assert expected.checks == None


# ======================== Resolve references for expected_commit.checks.cherry_pick attribute ========================
def testResolveReferences_givenCherryPickRef_expectCommitWithRef(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.cherry_pick = "branch1"
    validator.resolve_references_checks(expected)

    assert expected.checks.cherry_pick.message == "3. added branch1.md"

def testResolveReferences_givenCherryPickCommitRef_expectFoundCommit(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.cherry_pick = 1
    validator.resolve_references_checks(expected)

    assert expected.checks.cherry_pick.message == "1. added file1.md"

def testResolveReferences_givenCherryPickNotFound_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.cherry_pick = -1
    validator.resolve_references_checks(expected)

    assert isinstance(expected.checks.cherry_pick, NotFoundCommit)

def testResolveReferences_givenCherryPickNonExistingRef_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.cherry_pick = "inexistent"
    validator.resolve_references_checks(expected)

    assert isinstance(expected.checks.cherry_pick, NotFoundCommit)

def testResolveReferences_givenCherryPickItself_expectReferencedItself(validator):
    expected = ExpectedCommit(1)
    expected.checks = Checks()
    expected.checks.cherry_pick = 1
    validator.resolve_references_checks(expected)

    assert isinstance(expected.checks.cherry_pick, ReferencedItselfCommit)

# ======================== Resolve references for expected_commit.checks.reverts attribute ========================
def testResolveReferences_givenRevertsRef_expectCommitWithRef(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.reverts = "branch1"
    validator.resolve_references_checks(expected)

    assert expected.checks.reverts.message == "3. added branch1.md"

def testResolveReferences_givenRevertsCommitRef_expectFoundCommit(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.reverts = 1
    validator.resolve_references_checks(expected)

    assert expected.checks.reverts.message == "1. added file1.md"

def testResolveReferences_givenRevertsNotFound_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.reverts = -1
    validator.resolve_references_checks(expected)

    assert isinstance(expected.checks.reverts, NotFoundCommit)

def testResolveReferences_givenRevertsNonExistingRef_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.reverts = "inexistent"
    validator.resolve_references_checks(expected)

    assert isinstance(expected.checks.reverts, NotFoundCommit)

def testResolveReferences_givenRevertsItself_expectReferencedItself(validator):
    expected = ExpectedCommit(1)
    expected.checks = Checks()
    expected.checks.reverts = 1
    validator.resolve_references_checks(expected)

    assert isinstance(expected.checks.reverts, ReferencedItselfCommit)

# ======================== Resolve references for expected_commit.checks.squashes attribute ========================
def testResolveReferences_givenSquashesRef_expectCommitWithRef(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.squashes = ["branch1", "branch2"]
    validator.resolve_references_checks(expected)

    assert expected.checks.squashes[0].message == "3. added branch1.md"
    assert expected.checks.squashes[1].message == "4. added branch2.md"

def testResolveReferences_givenSquashesCommitRef_expectFoundCommit(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.squashes = [1, 2]
    validator.resolve_references_checks(expected)

    assert expected.checks.squashes[0].message == "1. added file1.md"
    assert expected.checks.squashes[1].message == "2. modified file1.md"

def testResolveReferences_givenSquashesNotFound_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.squashes = [-1]
    validator.resolve_references_checks(expected)

    assert isinstance(expected.checks.squashes[0], NotFoundCommit)

def testResolveReferences_givenSquashesNonExistingRef_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.squashes = ["inexistent"]
    validator.resolve_references_checks(expected)

    assert isinstance(expected.checks.squashes[0], NotFoundCommit)

def testResolveReferences_givenSquashesItself_expectReferencedItself(validator):
    expected = ExpectedCommit(1)
    expected.checks = Checks()
    expected.checks.squashes = [1]
    validator.resolve_references_checks(expected)

    assert isinstance(expected.checks.squashes[0], ReferencedItselfCommit)


def testResolveReferences_givenSquashesByBranch_expectListOfCommits(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.squashes = "squash-branch"
    commit = validator.repo.find_commit_by_ref("Squashed")
    validator.resolve_references_checks(expected, commit)

    assert len(expected.checks.squashes) == 2
    assert expected.checks.squashes[0].message == "5. first change to file1.md"
    assert expected.checks.squashes[1].message == "6. second change to file1.md"
