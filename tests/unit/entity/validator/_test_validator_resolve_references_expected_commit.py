import pytest

from gitjudge.entity import Validator, Checks, CommitDefinition, Commit, NotFoundCommit, ReferencedItselfCommit

def testResolveReferences_givenNothing_expectNoChange(validator):
    expected = CommitDefinition("id")
    validator.resolve_references_expected_commit(expected)

    assert expected.start == None
    assert expected.end == None
    assert expected.checks == None


# ======================== Resolve references for expected_commit.start attribute ========================
def testResolveReferences_givenRefStart_expectCommitWithRef(validator):
    expected = CommitDefinition("id")
    expected.start = "branch1"
    validator.resolve_references_expected_commit(expected)

    assert expected.start.message == "3. added branch1.md"

def testResolveReferences_givenCommitRefStart_expectFoundCommit(validator):
    expected = CommitDefinition("id")
    expected.start = 1
    validator.resolve_references_expected_commit(expected)

    assert expected.start.message == "1. added file1.md"

def testResolveReferences_givenNotFoundStart_expectNotFound(validator):
    expected = CommitDefinition("id")
    expected.start = -1
    validator.resolve_references_expected_commit(expected)

    assert isinstance(expected.start, NotFoundCommit)

def testResolveReferences_givenNonExistingRef_expectNotFound(validator):
    expected = CommitDefinition("id")
    expected.start = "inexistent"
    validator.resolve_references_expected_commit(expected)

    assert isinstance(expected.start, NotFoundCommit)

def testResolveReferences_givenItselfStart_expectReferencedItself(validator):
    expected = CommitDefinition(1)
    expected.start = 1
    validator.resolve_references_expected_commit(expected)

    assert isinstance(expected.start, ReferencedItselfCommit)


# ======================== Resolve references for expected_commit.end attribute ========================
def testResolveReferences_givenRefEnd_expectCommitWithRef(validator):
    expected = CommitDefinition("id")
    expected.end = "branch1"
    validator.resolve_references_expected_commit(expected)

    assert expected.end.message == "3. added branch1.md"

def testResolveReferences_givenCommitRefEnd_expectFoundCommit(validator):
    expected = CommitDefinition("id")
    expected.end = 1
    validator.resolve_references_expected_commit(expected)

    assert expected.end.message == "1. added file1.md"

def testResolveReferences_givenNotFoundEnd_expectNotFound(validator):
    expected = CommitDefinition("id")
    expected.end = -1
    validator.resolve_references_expected_commit(expected)

    assert isinstance(expected.end, NotFoundCommit)

def testResolveReferences_givenNonExistingRefEnd_expectNotFound(validator):
    expected = CommitDefinition("id")
    expected.end = "inexistent"
    validator.resolve_references_expected_commit(expected)

    assert isinstance(expected.end, NotFoundCommit)

def testResolveReferences_givenItselfEnd_expectReferencedItself(validator):
    expected = CommitDefinition(1)
    expected.end = 1
    validator.resolve_references_expected_commit(expected)

    assert isinstance(expected.end, ReferencedItselfCommit)
