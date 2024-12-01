import pytest

from gitjudge.mapper.commit_definition import map_commit_definition
from gitjudge.entity.commit_definition import CommitDefinition


def testMap_givenWrongType_shouldRaiseError():
    with pytest.raises(TypeError):
        map_commit_definition(1, 1)


def testMap_givenEmptyDictWithId_shouldReturnCommitDefinition():
    commit_definition_dict = {}
    commit_definition = map_commit_definition("1", commit_definition_dict)
    assert isinstance(commit_definition, CommitDefinition)
    assert commit_definition.id == "1"


def testMap_givenDictWithMessage_messageShouldBeSet():
    commit_definition_dict = {"message": "Message"}
    commit_definition = map_commit_definition("1", commit_definition_dict)
    assert commit_definition.message == "Message"


def testMap_givenDictWithStart_startingPointShouldBeSet():
    commit_definition_dict = {"start": "main"}
    commit_definition = map_commit_definition("1", commit_definition_dict)
    assert commit_definition.start == "main"
