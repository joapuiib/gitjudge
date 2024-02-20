import pytest
from gitjudge.entity import ExpectedCommit

def test_givenConstructorWithoutID_shouldThrowError():
    with pytest.raises(TypeError):
        ExpectedCommit()

def test_commitConstructorShouldHaveID():
    commit = ExpectedCommit(1)
    assert commit.id == 1
    assert commit.message == None
    assert commit.start == None
    assert commit.end == None
    assert commit.checks == None

def test_givenSetMessage_shouldSetMessage():
    commit = ExpectedCommit(1, message="message")
    assert commit.message == "message"

def test_givenStart_shouldSetStart():
    commit = ExpectedCommit(1, start = "main")
    assert commit.start == "main"

def test_givenEnd_shouldSetEnd():
    commit = ExpectedCommit(1, end = "main")
    assert commit.end == "main"
