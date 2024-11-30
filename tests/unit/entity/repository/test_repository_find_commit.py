import pytest

from gitjudge.entity.commit import Commit, NotFoundCommit, ReferencedItselfCommit
from gitjudge.entity.commit_definition import CommitDefinition
from gitjudge.entity.diffindex import DiffIndex
from gitjudge.entity.difflist import DiffList

def testFindCommit_GivenNonCommitDefinitionParameter_ShouldRaiseError(empty_repo):
    with pytest.raises(TypeError):
        empty_repo.find_commit(1)


def testFindCommit_GivenEmptyRepo_ShouldReturnNone(empty_repo):
    expected_commit = CommitDefinition("1")
    assert empty_repo.find_commit(expected_commit) == None


"""
* c5bf0d3 - (0 seconds ago) 3. added branch1.md - Joan Puigcerver (branch1)
| * 57b1900 - (0 seconds ago) 4. added branch2.md - Joan Puigcerver (branch2.2, branch2)
|/
| * 6dbc914 - (0 seconds ago) 6. Cherry-pick "2. modified file1.md" - Joan Puigcerver (revert-cherry)
| * ebf5774 - (0 seconds ago) 5. Revert "2. modified file1.md" - Joan Puigcerver
|/
| * f533136 - (0 seconds ago) 8. second change squash - Joan Puigcerver (squash-branch)
| * a692df0 - (0 seconds ago) 7. first change squash - Joan Puigcerver
|/
| * 646b91a - (0 seconds ago) 9. Squashed changes to file1.md - Joan Puigcerver (tag: squashed, squashed)
|/
* 7cb78bd - (0 seconds ago) 2. modified file1.md - Joan Puigcerver (HEAD -> main, tag: T3, tag: T2)
* 27f0b5f - (0 seconds ago) 1. added file1.md - Joan Puigcerver (tag: T1)
"""

def testFindCommit_GivenNonExistingCommit_ShouldReturnCommit(repo):
    # Arrange
    expected_commit = CommitDefinition("0")
    expected_commit.message = "0."

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert isinstance(result, NotFoundCommit)
    assert result.id == "0"


def testFindCommit_GivenExistingCommit_ShouldReturnCommit(repo):
    # Arrange
    expected_commit = CommitDefinition("1")
    expected_commit.message = "1."

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert isinstance(result, Commit)
    assert result.id == "1"
    assert len(result.hash) > 0
    assert result.message == "1. added file1.md"
    assert result.diff == DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"1": 1},
        )
    })


def testFindCommit_GivenPatterMessage_ShouldReturnCommit(repo):
    # Arrange
    expected_commit = CommitDefinition("1")
    expected_commit.message = "1.[ ]*added"

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert isinstance(result, Commit)
    assert result.id == "1"
    assert len(result.hash) > 0
    assert result.message == "1. added file1.md"


def testFindCommit_GivenExistingCommitThatIsNotInDefaultBranch_ShouldReturnNone(repo):
    # Arrange
    expected_commit = CommitDefinition("3")
    expected_commit.message = "3."

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert isinstance(result, NotFoundCommit)
    assert result.id == "3"



def testFindCommit_GivenExistingCommitThatInSpecificStart_ShouldReturnCommit(repo):
    # Arrange
    expected_commit = CommitDefinition("3")
    expected_commit.message = "3."
    expected_commit.start = "branch1"

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert result.id == "3"
    assert result.message == "3. added branch1.md"


def testFindCommit_GivenExistingCommitOlderThanEnd_ShouldReturnNone(repo):
    # Arrange
    expected_commit = CommitDefinition("1")
    expected_commit.message = "1."
    expected_commit.end = "T2"

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert isinstance(result, NotFoundCommit)
    assert result.id == "1"


def testFindCommit_GivenExistingCommitOlderThanEnd_ShouldReturnCommit(repo):
    # Arrange
    expected_commit = CommitDefinition("2")
    expected_commit.message = "2."
    expected_commit.end = "T1"

    # Act
    result = repo.find_commit(expected_commit)

    print(repr(result.diff))


    # Assert
    assert result.id == "2"
    assert result.message == "2. modified file1.md"
    assert result.diff == DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"2": 1},
            deletions={}
        )
    })


def testFindCommit_GivenExistingCommitStartEndReverseOrder_ShouldReturnOlder(repo):
    # Arrange
    expected_commit = CommitDefinition("1")
    expected_commit.message = ".*file1.md.*"
    expected_commit.start = "T1"
    expected_commit.end = "HEAD"

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert result.id == "1"
    assert result.message == "1. added file1.md"


def testFindCommit_GivenExistingCommitStartEnd_ShouldReturnNewer(repo):
    # Arrange
    expected_commit = CommitDefinition("2")
    expected_commit.message = "[12]"
    expected_commit.start = "HEAD"
    expected_commit.end = "T1"

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert result.id == "2"
    assert result.message == "2. modified file1.md"


def testFindCommit_GivenUnrelatedStartEnd_ShouldRaiseError(repo):
    # Arrange
    expected_commit = CommitDefinition("2")
    expected_commit.message = "2."
    expected_commit.start = "branch1"
    expected_commit.end = "branch2"

    # Act
    with pytest.raises(ValueError):
        repo.find_commit(expected_commit)


def testFindCommit_GivenCommitWithTag_ShouldReturnCommitWithTags(repo):
    # Arrange
    expected_commit = CommitDefinition("1")
    expected_commit.message = "1."

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert result.tags == ["T1"]


def testFindCommit_GivenCommitWithMultipleTags_ShouldReturnCommitWithTags(repo):
    # Arrange
    expected_commit = CommitDefinition("2")
    expected_commit.message = "2."

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert result.tags == ["T2", "T3"]


def testFindCommit_GivenCommitWithNoTags_ShouldReturnCommitWithNoTags(repo):
    # Arrange
    expected_commit = CommitDefinition("3")
    expected_commit.message = "3."
    expected_commit.start = "branch1"

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert result.tags == []

def testFindCommit_GivenCommitWithNotFoundStart_ShouldReturnNotFound(repo):
    # Arrange
    expected_commit = CommitDefinition("1")
    expected_commit.message = "1."
    expected_commit.start = NotFoundCommit(0)

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert isinstance(result, NotFoundCommit)
    assert result.id == "1"

def testFindCommit_GivenCommitWithReferencedItselfStart_ShouldReturnReferencedItself(repo):
    # Arrange
    expected_commit = CommitDefinition("1")
    expected_commit.message = "1."
    expected_commit.start = ReferencedItselfCommit(0)

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert isinstance(result, ReferencedItselfCommit)
    assert result.id == "1"

def testFindCommit_GivenCommitWithNotFoundEnd_ShouldReturnNotFound(repo):
    # Arrange
    expected_commit = CommitDefinition("1")
    expected_commit.message = "1."
    expected_commit.end = NotFoundCommit(0)

    # Act
    result = repo.find_commit(expected_commit)

    # Assert
    assert isinstance(result, NotFoundCommit)
    assert result.id == "1"
