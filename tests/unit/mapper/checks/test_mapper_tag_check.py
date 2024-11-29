import pytest
from gitjudge.mapper.checks.tag_check import map_tag_check
from gitjudge.entity.checks import TagCheck

def test_givenDictWithTagAndTags_shouldRaiseError():
    d = {'tag': 'tag', 'tags': ['tag1', 'tag2']}
    with pytest.raises(ValueError):
        map_tag_check(d)

def test_givenDictWithNoTagOrTags_shouldReturnEmptyList():
    d = {}
    checks = map_tag_check(d)
    assert checks == []

def test_givenDictWithTag_shouldCreateTagCheck():
    d = {'tag': 'tag'}
    checks = map_tag_check(d)
    assert len(checks) == 1
    assert isinstance(checks[0], TagCheck)
    assert list(checks[0].tags.keys()) == ['tag']


def test_givenDictWithTags_shouldCreateTagCheck():
    d = {'tags': ['tag1', 'tag2']}
    checks = map_tag_check(d)
    assert len(checks) == 1
    assert isinstance(checks[0], TagCheck)
    assert list(checks[0].tags.keys()) == ['tag1', 'tag2']
