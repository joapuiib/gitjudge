import pytest
from gitjudge.entity import ExpectedCommit

def test_givenConstructorWithoutID_shouldThrowError():
    with pytest.raises(TypeError):
        ExpectedCommit()

def test_commitConstructorShouldHaveID():
    commit = ExpectedCommit(1)
    assert commit.id == 1
    assert commit.message == None
    assert commit.starting_point == None
    assert commit.parents == []
    assert commit.branches == []
    assert commit.tags == []
    assert commit.checks == None

def test_givenSetMessage_shouldSetMessage():
    commit = ExpectedCommit(1, message="message")
    assert commit.message == "message"

def test_givenStartingPoint_shouldSetStartingPoint():
    commit = ExpectedCommit(1, starting_point="main")
    assert commit.starting_point == "main"
