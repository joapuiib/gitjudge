import pytest
from gitjudge.entity import Validator

def test_givenValidatorWhithoutArgs_shouldRaiseError():
    with pytest.raises(TypeError):
        Validator()

def test_givenWithWrongType_shouldRaiseError():
    with pytest.raises(TypeError):
        Validator("wrong_type")

def test_givenRepoAndDefinition_shouldCreateValidator(repo, definition):
    validator = Validator(repo, definition, {})
    assert validator.repo == repo
    assert validator.definition == definition
    assert validator.args == {}
    assert validator.found_commits == {}
