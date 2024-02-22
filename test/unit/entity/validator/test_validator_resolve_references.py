import pytest

from gitjudge.entity import Validator, Checks, ExpectedCommit, Commit

def testResolveReferences_givenNothing_expectNoChange(validator):
    expected = ExpectedCommit("id")
    validator.resolve_references(expected)

    assert expected.start == None
    assert expected.end == None
    assert expected.checks == None


# ======================== Resolve references for expected_commit.start attribute ========================
def testResolveReferences_givenRefStart_expectCommitWithRef(validator):
    expected = ExpectedCommit("id")
    expected.start = "branch1"
    validator.resolve_references(expected)

    assert expected.start.message == "3. added branch1.md"

def testResolveReferences_givenCommitRefStart_expectFoundCommit(validator):
    expected = ExpectedCommit("id")
    expected.start = 1
    validator.resolve_references(expected)

    assert expected.start.message == "1. added file1.md"

def testResolveReferences_givenNotFoundStart_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.start = -1
    validator.resolve_references(expected)

    assert expected.start is Commit.NotFoundCommit

def testResolveReferences_givenNonExistingRef_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.start = "inexistent"
    validator.resolve_references(expected)

    assert expected.start is Commit.NotFoundCommit

def testResolveReferences_givenItselfStart_expectReferencedItself(validator):
    expected = ExpectedCommit(1)
    expected.start = 1
    validator.resolve_references(expected)

    assert expected.start is Commit.ReferencedItselfCommit


# ======================== Resolve references for expected_commit.end attribute ========================
def testResolveReferences_givenRefEnd_expectCommitWithRef(validator):
    expected = ExpectedCommit("id")
    expected.end = "branch1"
    validator.resolve_references(expected)

    assert expected.end.message == "3. added branch1.md"

def testResolveReferences_givenCommitRefEnd_expectFoundCommit(validator):
    expected = ExpectedCommit("id")
    expected.end = 1
    validator.resolve_references(expected)

    assert expected.end.message == "1. added file1.md"

def testResolveReferences_givenNotFoundEnd_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.end = -1
    validator.resolve_references(expected)

    assert expected.end is Commit.NotFoundCommit

def testResolveReferences_givenNonExistingRefEnd_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.end = "inexistent"
    validator.resolve_references(expected)

    assert expected.end is Commit.NotFoundCommit

def testResolveReferences_givenItselfEnd_expectReferencedItself(validator):
    expected = ExpectedCommit(1)
    expected.end = 1
    validator.resolve_references(expected)

    assert expected.end is Commit.ReferencedItselfCommit

# ======================== Resolve references for expected_commit.checks.cherry_pick attribute ========================
def testResolveReferences_givenCherryPickRef_expectCommitWithRef(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.cherry_pick = "branch1"
    validator.resolve_references(expected)

    assert expected.checks.cherry_pick.message == "3. added branch1.md"

def testResolveReferences_givenCherryPickCommitRef_expectFoundCommit(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.cherry_pick = 1
    validator.resolve_references(expected)

    assert expected.checks.cherry_pick.message == "1. added file1.md"

def testResolveReferences_givenCherryPickNotFound_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.cherry_pick = -1
    validator.resolve_references(expected)

    assert expected.checks.cherry_pick is Commit.NotFoundCommit

def testResolveReferences_givenCherryPickNonExistingRef_expectNotFound(validator):
    expected = ExpectedCommit("id")
    expected.checks = Checks()
    expected.checks.cherry_pick = "inexistent"
    validator.resolve_references(expected)

    assert expected.checks.cherry_pick is Commit.NotFoundCommit

def testResolveReferences_givenCherryPickItself_expectReferencedItself(validator):
    expected = ExpectedCommit(1)
    expected.checks = Checks()
    expected.checks.cherry_pick = 1
    validator.resolve_references(expected)

    assert expected.checks.cherry_pick is Commit.ReferencedItselfCommit
