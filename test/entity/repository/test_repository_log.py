import pytest

def testLog_GivenExistingRepo_ShouldReturnLog(repo):
    # Act
    log = repo.log()

    # Assert
    assert len(log) > 0
