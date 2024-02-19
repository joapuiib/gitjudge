import pytest

from gitjudge.entity import LogOptions

def testLogOptions_GivenEmptyOptions_ShouldHaveDefaultOptions():
    # Arrange
    options = LogOptions()

    # Assert
    assert options.branches is None
    assert options.all is False
