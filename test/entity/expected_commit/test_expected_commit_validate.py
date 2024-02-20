import pytest

from gitjudge.entity import Commit, ExpectedCommit, CheckResult

def test_validateNonCommit_shouldRaiseError():
    expected = ExpectedCommit("id")
    with pytest.raises(TypeError):
        expected.validate("not a commit")

def test_expectedCommitWithoutChecks_shouldValidate(mocker):
    expected = ExpectedCommit("id")
    commit = mocker.create_autospec(Commit)
    result = expected.validate(commit)

    assert isinstance(result, CheckResult)
    assert result.commit == commit

def test_expectedCommitWithChecks_shouldValidate(mocker):
    expected_result = {"tags": {"T": True}}
    mock_checks = mocker.Mock()
    mock_checks.validate.return_value = expected_result

    expected = ExpectedCommit("id")
    expected.checks = mock_checks

    commit = mocker.create_autospec(Commit)
    result = expected.validate(commit)

    mock_checks.validate.assert_called_with(commit)
    assert result == expected_result

