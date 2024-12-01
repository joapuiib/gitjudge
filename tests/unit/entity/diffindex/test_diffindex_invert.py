from gitjudge.entity.diffindex import DiffIndex


def test_invert_empty_diffindex():
    diff = DiffIndex("path")
    diff.invert()

    assert diff.file_path == "path"
    assert diff.additions == {}
    assert diff.deletions == {}


def test_invert_additions():
    diff = DiffIndex("path", additions={"line1": 1}, deletions={})

    diff.invert()

    assert diff.file_path == "path"
    assert diff.additions == {}
    assert diff.deletions == {"line1": 1}


def test_invert_deletions():
    diff = DiffIndex("path", additions={}, deletions={"line1": 1})

    diff.invert()

    assert diff.file_path == "path"
    assert diff.additions == {"line1": 1}
    assert diff.deletions == {}
