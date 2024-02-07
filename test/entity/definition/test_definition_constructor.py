import pytest
from datetime import datetime

from gitjudge.entity.definition import Definition
from gitjudge.entity.expected_commit import ExpectedCommit

def test_givenConstructorWithoutName_shouldRaiseError():
    with pytest.raises(TypeError):
        Definition()

def test_givenConstructorWithName_shouldCreateDefinition():
    definition = Definition("name")

    assert definition.name == "name"
    assert definition.limit_date == None
    assert definition.expected_commits == []

