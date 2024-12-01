import pytest
from gitjudge.entity.commit_definition import CommitDefinition


def test_givenConstructorWithoutID_shouldThrowError():
    with pytest.raises(TypeError):
        CommitDefinition()


def test_commitConstructorShouldHaveID():
    commit = CommitDefinition(1)
    assert commit.id == 1
    assert commit.message == None
    assert commit.start == None
    assert commit.end == None
    assert commit.checks == []


def test_givenSetMessage_shouldSetMessage():
    commit = CommitDefinition(1, message="message")
    assert commit.message == "message"


def test_givenStart_shouldSetStart():
    commit = CommitDefinition(1, start="main")
    assert commit.start == "main"


def test_givenEnd_shouldSetEnd():
    commit = CommitDefinition(1, end="main")
    assert commit.end == "main"
