import pytest

from gitjudge.entity.commit import Commit
from gitjudge.entity.difflist import DiffList
from gitjudge.entity.diffindex import DiffIndex

def test_giventNoCommits_shouldRaiseError():
    commit = Commit(1)
    with pytest.raises(TypeError):
        commit.reverts()


def test_givenCommitWithSameDiff_ShouldReturnTrue():
    commit = Commit(1, message="commit")
    commit.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    squash = Commit(2, message="commit")
    squash.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    assert commit.squashes([squash])


def test_givenCommitWithDifferentDiff_ShouldReturnFalse():
    commit = Commit(1, message="commit")
    commit.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    squash = Commit(2, message="commit")
    squash.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 2},
            deletions={}
        )
    })
    assert not commit.squashes([squash])


def test_givenCommitThatSquashesTwoCommits_ShouldReturnTrue():
    commit = Commit(1, message="commit")
    commit.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 2},
            deletions={}
        )
    })

    squash = Commit(2, message="commit")
    squash.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    squash2 = Commit(3, message="commit")
    squash2.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    assert commit.squashes([squash, squash2])

def test_givenCommitThatSquashesTwoCommitsDifferent_ShouldReturnFalse():
    commit = Commit(1, message="commit")
    commit.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 3},
            deletions={}
        )
    })

    squash = Commit(2, message="commit")
    squash.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    squash2 = Commit(3, message="commit")
    squash2.diff = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={}
        )
    })
    assert not commit.squashes([squash, squash2])
