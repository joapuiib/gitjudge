import pytest
from gitjudge.entity import Commit, DiffList

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
    assert isinstance(commit.diff, DiffList)

def test_commitConstructorWithMessage_shouldHaveMessage():
    commit = Commit(1, "message")
    assert commit.message == "message"

def test_commitConstructorWithTags_shouldHaveTags():
    commit = Commit(1, tags=["tag1", "tag2"])
    assert commit.tags == ["tag1", "tag2"]
