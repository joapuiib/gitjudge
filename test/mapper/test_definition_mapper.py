import pytest
from datetime import datetime

from gitjudge.mapper.definition import map_definition
from gitjudge.entity.definition import Definition
from gitjudge.entity.expected_commit import ExpectedCommit

def test_dictWithoutName_ShouldRaiseError():
    with pytest.raises(TypeError):
        map_definition({})

def test_dictWithName_ShouldCreateDefinition():
    d = {"name": "definition"}
    definition = map_definition(d)
    assert definition.name == "definition"

def test_dictInvalidLimitDate_ShouldRaiseError():
    d = {"name": "definition", "limit_date": "invalid"}
    with pytest.raises(TypeError):
        map_definition(d)

def test_dictLimitDate_ShouldCreateDefinition():
    d = {"name": "definition", "limit_date": "2019-01-01"}
    definition = map_definition(d)
    assert isinstance(definition.limit_date, datetime)
    assert definition.limit_date == datetime(2019, 1, 1)

def test_dictLimitDateWithTime_ShouldCreateDefinition():
    d = {"name": "definition", "limit_date": "2019-01-01 12:00"}
    definition = map_definition(d)
    assert isinstance(definition.limit_date, datetime)
    assert definition.limit_date == datetime(2019, 1, 1, 12, 0)

def test_dictLimitDateWithSeconds_ShouldCreateDefinition():
    d = {"name": "definition", "limit_date": "2019-01-01 12:00:00"}
    definition = map_definition(d)
    assert isinstance(definition.limit_date, datetime)
    assert definition.limit_date == datetime(2019, 1, 1, 12, 0, 0)

def test_dictNoExpectedCommits_ShouldBeEmptyList():
    d = {"name": "definition"}
    definition = map_definition(d)
    assert isinstance(definition.expected_commits, list)
    assert len(definition.expected_commits) == 0

def test_dictEmptyExpectedCommits_ShouldBeEmptyList():
    d = {"name": "definition", "expected_commits": []}
    definition = map_definition(d)
    assert isinstance(definition.expected_commits, list)
    assert len(definition.expected_commits) == 0

def test_dictWithExpectedCommits_ShouldCreateDefinition():
    expected_commit = {"id": "1", "message": "message"}
    d = {"name": "definition", "expected_commits": [expected_commit]}

    definition = map_definition(d)
    assert len(definition.expected_commits) == 1
    assert isinstance(definition.expected_commits[0], ExpectedCommit)
    assert definition.expected_commits[0].id == "1"
    assert definition.expected_commits[0].message == "message"
