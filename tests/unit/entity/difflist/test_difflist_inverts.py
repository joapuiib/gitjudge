import pytest

from gitjudge.entity import DiffList, DiffIndex

def test_invert_empty_difflist():
    difflist = DiffList()
    inverted = difflist.invert()

    assert difflist == inverted
    assert difflist is not inverted


def test_invert_additions():
    difflist = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={},
        ),
        "file2.md": DiffIndex(
            "file2.md",
            additions={"line2": 1},
            deletions={},
        )
    })

    inverted = difflist.invert()

    assert difflist.diffs["file1.md"].additions == {"line1": 1}
    assert difflist.diffs["file1.md"].deletions == {}
    assert difflist.diffs["file2.md"].additions == {"line2": 1}
    assert difflist.diffs["file2.md"].deletions == {}

    assert inverted.diffs["file1.md"].additions == {}
    assert inverted.diffs["file1.md"].deletions == {"line1": 1}
    assert inverted.diffs["file2.md"].additions == {}
    assert inverted.diffs["file2.md"].deletions == {"line2": 1}


def test_invert_deletions():
    difflist = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={},
            deletions={"line1": 1},
        ),
        "file2.md": DiffIndex(
            "file2.md",
            additions={},
            deletions={"line2": 1},
        )
    })

    inverted = difflist.invert()

    assert inverted.diffs["file1.md"].additions == {"line1": 1}
    assert inverted.diffs["file1.md"].deletions == {}
    assert inverted.diffs["file2.md"].additions == {"line2": 1}
    assert inverted.diffs["file2.md"].deletions == {}


def test_invert_multiple_files():
    difflist = DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1},
            deletions={"line2": 1},
        ),
        "file2.md": DiffIndex(
            "file2.md",
            additions={"line3": 1},
            deletions={"line4": 1},
        )
    })

    inverted = difflist.invert()

    assert inverted.diffs["file1.md"].additions == {"line2": 1}
    assert inverted.diffs["file1.md"].deletions == {"line1": 1}
    assert inverted.diffs["file2.md"].additions == {"line4": 1}
    assert inverted.diffs["file2.md"].deletions == {"line3": 1}
