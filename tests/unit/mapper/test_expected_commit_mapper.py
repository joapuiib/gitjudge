import pytest

from gitjudge.mapper import map_expected_commit
from gitjudge.entity import ExpectedCommit, Checks

def testMap_givenWrongType_shouldRaiseError():
    with pytest.raises(TypeError):
        map_expected_commit(1, 1)

def testMap_givenEmptyDictWithId_shouldReturnExpectedCommit():
    expected_commit_dict = {}
    expected_commit = map_expected_commit('1', expected_commit_dict)
    assert isinstance(expected_commit, ExpectedCommit)
    assert expected_commit.id == '1'

def testMap_givenEmptyMessage_shouldRaiseError():
    expected_commit_dict = {'message': None}
    with pytest.raises(ValueError):
        map_expected_commit(1, expected_commit_dict)

def testMap_givenDictWithMessage_messageShouldBeSet():
    expected_commit_dict = {'message': 'Message'}
    expected_commit = map_expected_commit('1', expected_commit_dict)
    assert expected_commit.message == 'Message'

def testMap_givenDictWithStart_startingPointShouldBeSet():
    expected_commit_dict = {'start': 'main'}
    expected_commit = map_expected_commit('1', expected_commit_dict)
    assert expected_commit.start == 'main'

def testMap_givenDictWithTwoTags_tagShouldBeList():
    expected_commit_dict = {'check': {"tag": "T1", "cherry-pick": "1"}}
    expected_commit = map_expected_commit('1', expected_commit_dict)
    assert isinstance(expected_commit.checks, Checks)
    assert expected_commit.checks.tags == ["T1"]
    assert expected_commit.checks.cherry_pick == "1"
