import pytest

from gitjudge.entity import DiffIndex

def test_create_diff():
    diff = DiffIndex("path")
    assert diff.file_path == "path"
    assert diff.additions == {}
    assert diff.deletions == {}


def test_add_addition():
    diff = DiffIndex("path")
    diff.add_addition("line")
    assert diff.additions == {"line": 1}
    diff.add_addition("line")
    assert diff.additions == {"line": 2}
    diff.add_addition("line")
    assert diff.additions == {"line": 3}


def test_add_deletion():
    diff = DiffIndex("path")
    diff.add_deletion("line")
    assert diff.deletions == {"line": 1}
    diff.add_deletion("line")
    assert diff.deletions == {"line": 2}
    diff.add_deletion("line")
    assert diff.deletions == {"line": 3}


def test_add_addition_and_deletion():
    diff = DiffIndex("path")
    diff.add_addition("line")
    assert diff.additions == {"line": 1}
    diff.add_addition("line")
    assert diff.additions == {"line": 2}
    diff.add_deletion("line")
    assert diff.additions == {"line": 1}
    diff.add_deletion("line")
    assert diff.additions == {}


def test_add_deletion_and_addition():
    diff = DiffIndex("path")
    diff.add_deletion("line")
    assert diff.deletions == {"line": 1}
    diff.add_deletion("line")
    assert diff.deletions == {"line": 2}
    diff.add_addition("line")
    assert diff.deletions == {"line": 1}
    diff.add_addition("line")
    assert diff.deletions == {}

def test_eq_emptyIndex():
    diff1 = DiffIndex("path")
    diff2 = DiffIndex("path")
    assert diff1 == diff2

def test_eq_sameIndex():
    diff1 = DiffIndex("path")
    diff1.add_addition("line1")
    diff1.add_deletion("line2")
    diff2 = DiffIndex("path")
    diff2.add_addition("line1")
    diff2.add_deletion("line2")
    assert diff1 == diff2

def test_merge_additions():
    diff1 = DiffIndex("path")
    diff1.add_addition("line1")
    diff2 = DiffIndex("path")
    diff1.add_addition("line1")

    diff1.merge(diff2)
    assert diff1.additions == {"line1": 2}

def test_merge_deletions():
    diff1 = DiffIndex("path")
    diff1.add_deletion("line1")
    diff2 = DiffIndex("path")
    diff1.add_deletion("line1")

    diff1.merge(diff2)
    assert diff1.deletions == {"line1": 2}

def test_merge_additions_and_deletions():
    diff1 = DiffIndex("path")
    diff1.add_addition("line1")
    diff2 = DiffIndex("path")
    diff1.add_deletion("line1")

    diff1.merge(diff2)
    assert diff1.additions == {}
    assert diff1.deletions == {}
