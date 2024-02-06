import pytest

from gitjudge.mapper.expected_commit import map_expected_commit
from gitjudge.entity.expected_commit import ExpectedCommit

def testMap_givenDictWithoutId_shouldRaiseError():
    with pytest.raises(ValueError):
        map_expected_commit({})

def testMap_givenDictWithId_shouldReturnExpectedCommit():
    expected_commit_dict = {'id': '1'}
    expected_commit = map_expected_commit(expected_commit_dict)
    assert isinstance(expected_commit, ExpectedCommit)
    assert expected_commit.id == '1'

def testMap_givenDictWithMessage_messageShouldBeSet():
    expected_commit_dict = {'id': '1', 'message': 'Message'}
    expected_commit = map_expected_commit(expected_commit_dict)
    assert expected_commit.message == 'Message'

def testMap_givenDictWithStartingPoint_startingPointShouldBeSet():
    expected_commit_dict = {'id': '1', 'starting_point': 'main'}
    expected_commit = map_expected_commit(expected_commit_dict)
    assert expected_commit.starting_point == 'main'

def testMap_givenDictWithoutParent_parentShouldBeEmptyList():
    expected_commit_dict = {'id': '1'}
    expected_commit = map_expected_commit(expected_commit_dict)
    assert expected_commit.parents == []

def testMap_givenDictWithSingleParent_parentShouldBeListSingle():
    expected_commit_dict = {'id': '1', 'parent': '2'}
    expected_commit = map_expected_commit(expected_commit_dict)
    assert expected_commit.parents == ['2']

def testMap_givenDictWithTwoParents_parentShouldBeList():
    expected_commit_dict = {'id': '1', 'parents': ['2', '3']}
    expected_commit = map_expected_commit(expected_commit_dict)
    assert expected_commit.parents == ['2', '3']

def testMap_givenDictWithMoreThanTwoParents_shouldRaiseError():
    with pytest.raises(ValueError):
        map_expected_commit({'id': '1', 'parents': ['2', '3', '4']})

def testMap_givenDictWithParentAndParents_shouldRaiseError():
    with pytest.raises(ValueError):
        map_expected_commit({'id': '1', 'parent': '2', 'parents': ['3']})

def testMap_givenDictWithoutTag_tagShouldBeEmptyList():
    expected_commit_dict = {'id': '1'}
    expected_commit = map_expected_commit(expected_commit_dict)
    assert expected_commit.tags == []

def testMap_givenDictWithSingleTag_tagShouldBeListSingle():
    expected_commit_dict = {'id': '1', 'tag': 'T'}
    expected_commit = map_expected_commit(expected_commit_dict)
    assert expected_commit.tags == ['T']

def testMap_givenDictWithTwoTags_tagShouldBeList():
    expected_commit_dict = {'id': '1', 'tags': ['T1', 'T2']}
    expected_commit = map_expected_commit(expected_commit_dict)
    assert expected_commit.tags == ['T1', 'T2']

def testMap_givenDictWithTagAndTags_shouldRaiseError():
    with pytest.raises(ValueError):
        map_expected_commit({'id': '1', 'tag': 'T1', 'tags': ['T2']})
