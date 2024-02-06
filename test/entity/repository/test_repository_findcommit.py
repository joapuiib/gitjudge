import pytest

from gitjudge.entity.commit import Commit
from gitjudge.entity.expected_commit import ExpectedCommit

def testFindCommit_GivenNonExpectedCommitParameter_ShouldRaiseError(empty_repo):
    with pytest.raises(TypeError):
        empty_repo.find_commit(1)

def testFindCommit_GivenEmptyRepo_ShouldReturnNone(empty_repo):
    expected_commit = ExpectedCommit("1")
    assert empty_repo.find_commit(expected_commit) == None

def testFindCommit_GivenNonExistingCommit_ShouldReturnCommit(repo):
    # Arrange
    expected_commit = ExpectedCommit("0")
    expected_commit.message = "0."

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert result == None

def testFindCommit_GivenExistingCommit_ShouldReturnCommit(repo):
    # Arrange
    expected_commit = ExpectedCommit("1")
    expected_commit.message = "1."

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert isinstance(result, Commit)
    assert result.id == "1"
    assert len(result.hash) > 0
    assert result.message == "1. added file1.md"

def testFindCommit_GivenWrongParentCommit_ShouldRaiseError(repo):
    # Arrange
    expected_commit = ExpectedCommit("2")
    expected_commit.message = "2."

    # Act
    with pytest.raises(TypeError):
        repo.find_commit(expected_commit, parent_commit="1")


def testFindCommit_GivenACommitThatIsNotChildOfParent_ShouldReturnNone(repo):
    # Arrange
    parent_expected_commit = ExpectedCommit("2")
    parent_expected_commit.message = "2."
    parent = repo.find_commit(parent_expected_commit)

    expected_commit = ExpectedCommit("1")
    expected_commit.message = "1."

    # Act
    result = repo.find_commit(expected_commit, parent_commit=parent)

    # Assert
    assert result == None

def testFindCommit_GivenExistingCommitThatIsNotInStartingPointBranch_ShouldReturnNone(repo):
    # Arrange
    expected_commit = ExpectedCommit("3")
    expected_commit.message = "3."

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert result == None

def testFindCommit_GivenExistingCommitThatInSpecificStartingPoint_ShouldReturnCommit(repo):
    # Arrange
    expected_commit = ExpectedCommit("3")
    expected_commit.message = "3."
    expected_commit.starting_point = "branch1"

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert result.id == "3"
    assert result.message == "3. added branch1.md"

