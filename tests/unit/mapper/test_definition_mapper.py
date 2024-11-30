import pytest
from datetime import datetime

from gitjudge.mapper.definition import map_definition
from gitjudge.entity.definition import Definition
from gitjudge.entity.commit_definition import CommitDefinition

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

def test_dictNoCommitDefinitions_ShouldBeEmptyList():
    d = {"name": "definition"}
    definition = map_definition(d)
    assert definition.commits == []

def test_dictEmptyCommitDefinitions_ShouldBeEmptyList():
    d = {"name": "definition", "commits": {}}
    definition = map_definition(d)
    assert definition.commits == []

def test_dictWithCommitDefinitions_ShouldCreateDefinition():
    commit_definition = {"message": "message"}
    d = {"name": "definition", "commits": {"1": commit_definition}}

    definition = map_definition(d)
    assert len(definition.commits) == 1
    assert isinstance(definition.commits[0], CommitDefinition)
    assert definition.commits[0].id == "1"
    assert definition.commits[0].message == "message"

def test_dictWithLogOptions_ShouldCreateDefinition():
    d = {"name": "definition", "log": {"branches": ["branch1"], "all": True}}
    definition = map_definition(d)
    assert definition.log_options.branches == ["branch1"]
    assert definition.log_options.all is True
