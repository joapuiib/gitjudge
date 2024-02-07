import pytest

from gitjudge.entity import Checks

def test_chekcsValidate_WrongParameters_ShouldRaiseError():
    checks = Checks()
    with pytest.raises(TypeError):
        checks.validate("not a commit")

