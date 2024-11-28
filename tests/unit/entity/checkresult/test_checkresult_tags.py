import pytest
from gitjudge.entity import CheckResult, Commit

def test_add_found_tag():
    commit = Commit(1)
    check_result = CheckResult(commit)
    check_result.add_tag("tag1", True)
    assert check_result.tags == {"tag1": True}
    assert check_result.is_correct()

def test_add_not_found_tag():
    commit = Commit(1)
    check_result = CheckResult(commit)
    check_result.add_tag("tag1", False)
    assert check_result.tags == {"tag1": False}
    assert not check_result.is_correct()

def test_add_multiple_tags():
    commit = Commit(1)
    check_result = CheckResult(commit)
    check_result.add_tag("tag1", True)
    check_result.add_tag("tag2", False)
    assert check_result.tags == {"tag1": True, "tag2": False}
    assert not check_result.is_correct()

def test_add_multiple_tags_correct():
    commit = Commit(1)
    check_result = CheckResult(commit)
    check_result.add_tag("tag1", True)
    check_result.add_tag("tag2", True)
    assert check_result.tags == {"tag1": True, "tag2": True}
    assert check_result.is_correct()
