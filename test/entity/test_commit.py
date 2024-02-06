import pytest
from gitjudge.entity.commit import Commit

def test_givenConstructorWithoutID_shouldRaiseError():
    with pytest.raises(TypeError):
        Commit()

def test_commitConstructorShouldHaveID():
    commit = Commit(1)
    assert commit.id == 1
    assert commit.hash == ""
    assert commit.message == ""
    assert commit.parents == []
    assert commit.branches == []
    assert commit.tags == []
