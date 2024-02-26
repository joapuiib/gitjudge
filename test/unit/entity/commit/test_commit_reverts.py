import pytest
from gitjudge.entity import Commit, DiffList, DiffIndex

def test_giventNoCommit_shouldRaiseError():
    commit = Commit(1)
    with pytest.raises(TypeError):
        commit.reverts()


def test_givenBothCommitsWithSameDiff_shouldReturnFalse():
    commit = Commit(1, message="commit")
    commit.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    reverted = Commit(2, message="commit")
    reverted.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    assert not reverted.reverts(commit)


def test_givenCommitWithAddition_AndRevertingWithDifferentDeletion_shouldReturnFalse():
    commit = Commit(1, message="commit")
    commit.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    reverted = Commit(2, message="commit")
    reverted.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={},
            deletions={"line2": 1}
        )
    })
    assert not reverted.reverts(commit)


def test_givenCommitWithAddition_AndRevertingWithSameDeletion_shouldReturnTrue():
    commit = Commit(1, message="commit")
    commit.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    reverted = Commit(2, message="commit")
    reverted.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={},
            deletions={"line1": 1}
        )
    })
    assert reverted.reverts(commit)


def test_givenCommitWithDeletion_AndRevertingWithDifferentAddition_shouldReturnFalse():
    commit = Commit(1, message="commit")
    commit.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={},
            deletions={"line1": 1}
        )
    })
    reverted = Commit(2, message="commit")
    reverted.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line2": 1},
            deletions={}
        )
    })
    assert not reverted.reverts(commit)


def test_givenCommitWithDeletion_AndRevertingWithSameAddition_shouldReturnTrue():
    commit = Commit(1, message="commit")
    commit.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={},
            deletions={"line1": 1}
        )
    })
    reverted = Commit(2, message="commit")
    reverted.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    assert reverted.reverts(commit)


def test_givenCommitWithMultipleAddition_AndRevertingWithSameDeletions_shouldReturnFalse():
    commit = Commit(1, message="commit")
    commit.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1, "line2": 1},
            deletions={}
        ),
        "file2.md": DiffIndex(
            "file2.md",
            additions={"line3": 1},
            deletions={}
        )
    })
    reverted = Commit(2, message="commit")
    reverted.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={},
            deletions={"line1": 1, "line2": 1}
        ),
        "file2.md": DiffIndex(
            "file2.md",
            additions={},
            deletions={"line3": 1}
        )
    })
    assert reverted.reverts(commit)
