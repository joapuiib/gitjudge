import re


def testLog_GivenExistingRepo_ShouldReturnLog(repo):
    # Act
    log = repo.log()

    # Assert
    assert len(log) > 0


def testLog_GivenBranches_ShouldShowBranches(repo):
    # Arrange
    branches = ["branch1"]

    # Act
    log = repo.log(branches=branches)

    # Assert
    assert re.search(r"\(.*branch1.*\)", log) is not None
    assert re.search(r"\(.*branch2.*\)", log) is None


def testLog_GivenMultipleBranches_ShouldShowBranches(repo):
    # Arrange
    branches = ["branch1", "branch2"]

    # Act
    log = repo.log(branches=branches)

    # Assert
    assert re.search(r"\(.*branch1.*\)", log) is not None
    assert re.search(r"\(.*branch2.*\)", log) is not None
