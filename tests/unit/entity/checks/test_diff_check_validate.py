import pytest

from gitjudge.entity.checks import DiffCheck
from gitjudge.entity.diffindex import DiffIndex
from gitjudge.entity.difflist import DiffList

"""
* ae33661 - (0 seconds ago) 3. added branch1.md - Joan Puigcerver (branch1)
| * 058a064 - (0 seconds ago) 4. added branch2.md - Joan Puigcerver (branch2)
|/
* 8ba96a6 - (0 seconds ago) 2. modified file1.md - Joan Puigcerver (HEAD -> main, tag: T3, tag: T2)
* 1ebb397 - (0 seconds ago) 1. added file1.md - Joan Puigcerver (tag: T1)
"""
repo = None

def test_hasDiff_shouldBeCorrect(found_commits):
    check = DiffCheck(
        diff=DiffList({
            "file1.md": DiffIndex(
                "file1.md",
                additions={"1": 1}
            )
        })
    )
    commit = found_commits[1]

    correct = check.validate(commit, repo)
    assert correct
    assert check.correct


def test_hasNotDiff_shouldBeNotCorrect(found_commits):
    check = DiffCheck(
        diff=DiffList({
            "file1.md": DiffIndex(
                "file1.md",
                additions={"1": 2}
            )
        })
    )
    commit = found_commits[1]

    correct = check.validate(commit, repo)
    assert not correct
    assert not check.correct
