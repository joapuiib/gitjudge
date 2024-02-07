import pytest

from gitjudge.mapper import map_checks
from gitjudge.entity import Checks

def testMap_givenWrongType_shouldRaiseError():
    with pytest.raises(TypeError):
        map_checks(1)

def testMap_givenEmptyDict_shouldReturnEmptyCheck():
    expected_checks_dict = {}
    checks = map_checks(expected_checks_dict)
    assert isinstance(checks, Checks)

def testMap_givenDictWithoutParent_parentShouldBeEmptyList():
    expected_checks_dict = {}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.parents == []

def testMap_givenDictWithSingleParent_parentShouldBeListSingle():
    expected_checks_dict = {'parent': '2'}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.parents == ['2']

def testMap_givenDictWithTwoParents_parentShouldBeList():
    expected_checks_dict = {'parents': ['2', '3']}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.parents == ['2', '3']

def testMap_givenDictWithMoreThanTwoParents_shouldRaiseError():
    with pytest.raises(ValueError):
        map_checks({'parents': ['2', '3', '4']})

def testMap_givenDictWithParentAndParents_shouldRaiseError():
    with pytest.raises(ValueError):
        map_checks({'parent': '2', 'parents': ['3']})

def testMap_givenDictWithoutTag_tagShouldBeEmptyList():
    expected_checks_dict = {}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.tags == []

def testMap_givenDictWithSingleTag_tagShouldBeListSingle():
    expected_checks_dict = {'tag': 'T'}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.tags == ['T']

def testMap_givenDictWithTwoTags_tagShouldBeList():
    expected_checks_dict = {'tags': ['T1', 'T2']}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.tags == ['T1', 'T2']

def testMap_givenDictWithTagAndTags_shouldRaiseError():
    with pytest.raises(ValueError):
        map_checks({'tag': 'T1', 'tags': ['T2']})

def testMap_givenDictWithCherryPick_shouldSetCherryPick():
    expected_checks_dict = {'cherry-pick': '1'}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.cherry_pick == '1'
