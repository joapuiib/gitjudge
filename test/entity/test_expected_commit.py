import pytest
from gitjudge.entity.expected_commit import ExpectedCommit

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
