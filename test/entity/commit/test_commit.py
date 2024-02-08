import pytest
from gitjudge.entity import Commit

def test_givenConstructorWithoutID_shouldRaiseError():
    with pytest.raises(TypeError):
        Commit()

def test_commitConstructorWithId_shouldHaveDefaultValues():
    commit = Commit(1)
    assert commit.id == 1
    assert commit.hash == ""
    assert commit.message == ""
    assert commit.parents == []
    assert commit.branches == []
    assert commit.tags == []
    assert commit._diff == ""

def test_commitConstructorWithMessage_shouldHaveMessage():
    commit = Commit(1, "message")
    assert commit.message == "message"

def test_commitConstructorWithDiff_shouldHaveDiff():
    commit = Commit(1, diff="diff")
    assert commit._diff == "diff"
