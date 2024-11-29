import pytest

from gitjudge.entity.checks import TagCheck

"""
* ae33661 - (0 seconds ago) 3. added branch1.md - Joan Puigcerver (branch1)
| * 058a064 - (0 seconds ago) 4. added branch2.md - Joan Puigcerver (branch2)
|/
* 8ba96a6 - (0 seconds ago) 2. modified file1.md - Joan Puigcerver (HEAD -> main, tag: T3, tag: T2)
* 1ebb397 - (0 seconds ago) 1. added file1.md - Joan Puigcerver (tag: T1)
"""

def test_tagCheck_hasSingleTag_shouldBeCorrect(found_commits):
    tag_check = TagCheck(["T1"])
    commit = found_commits[1]
    repo = None
    correct = tag_check.validate(commit, repo)
    assert correct
    assert tag_check.tags == {"T1": True}


def test_tagCheck_hasSingleTag_shouldBeIncorrect(found_commits):
    tag_check = TagCheck(["T2"])
    commit = found_commits[1]
    repo = None
    correct = tag_check.validate(commit, repo)
    assert not correct
    assert tag_check.tags == {"T2": False}

def test_tagCheck_hasAllTags_shouldBeCorrect(found_commits):
    tag_check = TagCheck(["T2", "T3"])
    commit = found_commits[2]
    repo = None
    correct = tag_check.validate(commit, repo)
    assert correct
    assert tag_check.tags == {"T2": True, "T3": True}

def test_tagCheck_hasSomeTags_shouldBeIncorrect(found_commits):
    tag_check = TagCheck(["T2", "T4"])
    commit = found_commits[2]
    repo = None
    correct = tag_check.validate(commit, repo)
    assert not correct
    assert tag_check.tags == {"T2": True, "T4": False}
