import pytest

from gitjudge.mapper.log_options import map_log_options
from gitjudge.entity.log_options import LogOptions


def testMap_givenWrongType_ShouldRaiseError():
    # Arrange
    d = "not a dict"

    # Act
    with pytest.raises(TypeError):
        map_log_options(d)


def testMap_givenEmptyDict_ShouldReturnDefaultOptions():
    # Arrange
    d = {}

    # Act
    options = map_log_options(d)

    # Assert
    assert isinstance(options, LogOptions)
    assert options.branches is None
    assert options.all is False


def testMap_givenBranches_ShouldReturnOptionsWithBranches():
    # Arrange
    d = {"branches": ["branch1"]}

    # Act
    options = map_log_options(d)

    # Assert
    assert options.branches == ["branch1"]
    assert options.all is False


def testMap_givenAll_ShouldReturnOptionsWithAll():
    # Arrange
    d = {"all": True}

    # Act
    options = map_log_options(d)

    # Assert
    assert options.branches is None
    assert options.all is True
