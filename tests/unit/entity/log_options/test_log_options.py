from gitjudge.entity.log_options import LogOptions


def testLogOptions_GivenEmptyOptions_ShouldHaveDefaultOptions():
    # Arrange
    options = LogOptions()

    # Assert
    assert options.branches is None
    assert options.all is False
