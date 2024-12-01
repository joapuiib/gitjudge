from gitjudge.entity.diffindex import DiffIndex


def test_contains_empty():
    diff1 = DiffIndex("")
    diff2 = DiffIndex("")

    assert diff1.contains(diff2)


def test_contains_additions_same_file():
    diff1 = DiffIndex("path", additions={"line1": 2}, deletions={})

    diff2 = DiffIndex("path", additions={"line1": 1}, deletions={})

    assert diff1.contains(diff2)
    assert not diff2.contains(diff1)


def test_contains_additions_same_file_same_lines():
    diff1 = DiffIndex("path", additions={"line1": 2}, deletions={})

    diff2 = DiffIndex("path", additions={"line1": 2}, deletions={})

    assert diff1.contains(diff2)
    assert diff2.contains(diff1)


def test_contains_deletions_same_file():
    diff1 = DiffIndex("path", additions={}, deletions={"line1": 2})

    diff2 = DiffIndex("path", additions={}, deletions={"line1": 1})

    assert diff1.contains(diff2)
    assert not diff2.contains(diff1)
