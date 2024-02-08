import pytest
from gitjudge.entity import Commit

def test_giventNoCommit_shouldRaiseError():
    commit = Commit(1)
    with pytest.raises(TypeError):
        commit.reverts()

def test_givenBothCommitsWithSameDiff_shouldReturnFalse():
    commit = Commit(1, message="commit", diff="+diff")
    reverted = Commit(2, message="commit", diff="+diff")
    assert not reverted.reverts(commit)

def test_givenCommitWithAddition_AndRevertingWithDifferentDeletion_shouldReturnFalse():
    commit = Commit(1, message="commit", diff="+1")
    reverted = Commit(2, message="commit", diff="-2")
    assert not reverted.reverts(commit)

def test_givenCommitWithAddition_AndRevertingWithSameDeletion_shouldReturnTrue():
    commit = Commit(1, message="commit", diff="+1")
    reverted = Commit(2, message="commit", diff="-1")
    assert reverted.reverts(commit)

def test_givenCommitWithDeletion_AndRevertingWithDifferentAddition_shouldReturnFalse():
    commit = Commit(1, message="commit", diff="-1")
    reverted = Commit(2, message="commit", diff="+2")
    assert not reverted.reverts(commit)

def test_givenCommitWithDeletion_AndRevertingWithSameAddition_shouldReturnTrue():
    commit = Commit(1, message="commit", diff="-1")
    reverted = Commit(2, message="commit", diff="+1")
    assert reverted.reverts(commit)

def test_givenCommitWithMultipleAddition_AndRevertingWithSameDeletions_shouldReturnFalse():
    commit = Commit(1, message="commit", diff="+1\n+2")
    reverted = Commit(2, message="commit", diff="-1\n-2")
    assert reverted.reverts(commit)

def test_givenCommitWithMultipleAddition_AndRevertingWithDifferentDeletions_shouldReturnFalse():
    commit = Commit(1, message="commit", diff="+1\n+2")
    reverted = Commit(2, message="commit", diff="-1\n-3")
    assert not reverted.reverts(commit)


def test_givenCommitWithMultipleDeletion_AndRevertingWithSameAdditions_shouldReturnFalse():
    commit = Commit(1, message="commit", diff="-1\n-2")
    reverted = Commit(2, message="commit", diff="+1\n+2")
    assert reverted.reverts(commit)

def test_givenCommitWithMultipleDeletion_AndRevertingWithDifferentAdditions_shouldReturnFalse():
    commit = Commit(1, message="commit", diff="-1\n-2")
    reverted = Commit(2, message="commit", diff="+1\n+3")
    assert not reverted.reverts(commit)

def test_givenCommitWithMultipleAdditionAndDeletion_AndRevertingWithSameAdditionAndDeletion_shouldReturnFalse():
    commit = Commit(1, message="commit", diff="+1\n-2")
    reverted = Commit(2, message="commit", diff="-1\n+2")
    assert reverted.reverts(commit)
