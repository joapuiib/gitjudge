import pytest
from gitjudge.entity import Commit

def test_giventCommitWithNoDiff_thenEmptyDiffIsReturned():
    commit = Commit(1)
    assert commit.diff() == ""

def test_givenCommitWithDiff_thenDiffIsReturned():
    commit = Commit(1)
    commit._diff = "diff"
    assert commit.diff() == "diff"

def test_givenCommitWithColoredDiff_thenColoredDiffIsReturned():
    commit = Commit(1)
    commit._diff = "\x1b[31mdiff\x1b[0m"
    assert commit.diff(colored=True) == "\x1b[31mdiff\x1b[0m"

def test_givenCommitWithColoredDiff_thenDiffIsReturnedWithoutColor():
    commit = Commit(1)
    commit._diff = "\x1b[31mdiff\x1b[0m"
    assert commit.diff(colored=False) == "diff"
