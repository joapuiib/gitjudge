import pytest

from gitjudge.entity import Checks

def test_chekcs_should_have_default_values():
    c = Checks()
    assert c.tags == []
    assert c.branches == []
    assert c.cherry_pick == None

