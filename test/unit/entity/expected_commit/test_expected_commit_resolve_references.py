import pytest

from gitjudge.entity import ExpectedCommit

def testResolveReferences_givenNothing_expectNoChange(found_commits):
    expected = ExpectedCommit("id")
    expected.resolve_references(found_commits)

    assert expected.start == None
    assert expected.end == None

def testResolveReferences_givenNonIntStart_expectNoChange(found_commits):
    expected = ExpectedCommit("id")
    expected.start = "branch1"
    expected.resolve_references(found_commits)

    assert expected.start == "branch1"
    assert expected.end == None

def testResolveReferences_givenNonIntEnd_expectNoChange(found_commits):
    expected = ExpectedCommit("id")
    expected.end = "branch2"
    expected.resolve_references(found_commits)

    assert expected.start == None
    assert expected.end == "branch2"

def testResolveReferences_givenIntStart_expectResolved(found_commits):
    expected = ExpectedCommit("id")
    expected.start = 1
    expected.resolve_references(found_commits)

    assert expected.start == found_commits[1]

def testResolveReferences_givenIntEnd_expectResolved(found_commits):
    expected = ExpectedCommit("id")
    expected.end = 1
    expected.resolve_references(found_commits)

    assert expected.end == found_commits[1]

def testResolveReferences_givenNonExistingStart_shouldRaiseError(found_commits):
    expected = ExpectedCommit("id")
    expected.start = -1

    with pytest.raises(ValueError) as e:
        expected.resolve_references(found_commits)
