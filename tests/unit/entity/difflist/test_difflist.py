import pytest

from gitjudge.entity.diffindex import DiffIndex
from gitjudge.entity.difflist import DiffList


def test_create_diff():
    difflist = DiffList()
    assert difflist.diffs == {}

def test_add_diff():
    difflist = DiffList()
    diff = DiffIndex("path")
    difflist.add(diff)
    assert difflist.diffs == {"path": diff}

def test_eq_emptyList():
    difflist1 = DiffList()
    difflist2 = DiffList()
    assert difflist1 == difflist2

def test_eq_sameList():
    difflist1 = DiffList()
    diff1 = DiffIndex("path")
    diff1.add_addition("line1")
    difflist1.add(diff1)

    difflist2 = DiffList()
    diff2 = DiffIndex("path")
    diff2.add_addition("line1")
    difflist2.add(diff2)
    assert difflist1 == difflist2

def test_merge_emptyList():
    difflist1 = DiffList()
    difflist2 = DiffList()
    difflist1.merge(difflist2)
    assert difflist1.diffs == {}

def test_merge_sameList():
    difflist1 = DiffList()
    diff1 = DiffIndex("path")
    diff1.add_addition("line1")
    difflist1.add(diff1)

    difflist2 = DiffList()
    diff2 = DiffIndex("path")
    diff2.add_addition("line1")
    difflist2.add(diff2)

    difflist1.merge(difflist2)
    assert difflist1.diffs["path"].additions == {"line1": 2}
