import pytest

from gitjudge.entity.commit import Commit
from gitjudge.entity.difflist import DiffList
from gitjudge.entity.diffindex import DiffIndex


def test_giventNoCommit_shouldRaiseError():
    commit = Commit(1)
    with pytest.raises(TypeError):
        commit.is_cherry_picked_from()


def test_givenCommitWithNoCherryPick_shouldReturnFalse():
    commit = Commit(1, message="commit")
    assert not commit.is_cherry_picked_from(None)


def test_givenCommitWithEmptyDiff_shouldReturnFalse():
    commit = Commit(1, message="commit")
    commit2 = Commit(2, message="commit2")
    assert not commit.is_cherry_picked_from(commit2)


def test_givenCommitWithDifferentDiffs_shouldReturnFalse():
    commit = Commit(1, message="commit")
    commit.diff = DiffList(
        {"file1.md": DiffIndex("file1.md", {"additions": {"line1": 1}, "deletions": {}})}
    )
    commit2 = Commit(2, message="commit")
    commit2.diff = DiffList(
        {"file1.md": DiffIndex("file1.md", {"additions": {"line2": 1}, "deletions": {}})}
    )
    assert not commit.is_cherry_picked_from(commit2)


def test_givenCommitWithSameNameAndDiff_shouldReturnTrue():
    commit = Commit(1, message="commit")
    commit.diff = DiffList(
        {"file1.md": DiffIndex("file1.md", {"additions": {"line1": 1}, "deletions": {}})}
    )
    commit2 = Commit(2, message="commit")
    commit2.diff = DiffList(
        {"file1.md": DiffIndex("file1.md", {"additions": {"line1": 1}, "deletions": {}})}
    )
    assert commit.is_cherry_picked_from(commit2)
