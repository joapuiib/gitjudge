import pytest
from gitjudge.entity import Commit

def test_giventNoCommit_shouldRaiseError():
    commit = Commit(1)
    with pytest.raises(TypeError):
        commit.is_cherry_picked_from()

def test_givenCommitWithDifferentNames_shouldReturnFalse():
    commit = Commit(1, message="commit")
    commit2 = Commit(2, message="commit2")
    assert not commit.is_cherry_picked_from(commit2)

def test_givenCommitWithDifferentDiffs_shouldReturnFalse():
    commit = Commit(1, message="commit", diff="diff")
    commit2 = Commit(2, message="commit", diff="diff2")
    assert not commit.is_cherry_picked_from(commit2)

def test_givenCommitWithSameNameAndDiff_shouldReturnTrue():
    commit = Commit(1, message="commit", diff="diff")
    commit2 = Commit(2, message="commit", diff="diff")
    assert commit.is_cherry_picked_from(commit2)
