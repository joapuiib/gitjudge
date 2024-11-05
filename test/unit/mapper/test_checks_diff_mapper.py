import pytest

from gitjudge.mapper import map_checks
from gitjudge.entity import Checks
from gitjudge.entity import DiffList, DiffIndex

def testMap_givenEmptyDiffDict_shouldReturnEmptyDiffList():
    diff = {}
    expected_checks_dict = {'diff': diff}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.diff == None

def testMap_givenDiffDictFilename_shouldReturnDiffList():
    diff = {"file1.md": ""}
    expected_checks_dict = {'diff': diff}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.diff == DiffList({
        "file1.md": DiffIndex(
            "file1.md"
        )
    })

def testMap_givenDiffDictFilenameSingleLine_shouldReturnDiffList():
    diff = {"file1.md": "+line1"}
    expected_checks_dict = {'diff': diff}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.diff == DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 1}
        )
    })

def testMap_givenDictWithDiff_shouldReturnDiffList():
    diff = {
        "file1.md": """
+line1
+line1
+line2
-line3
-line3
-line4
                    """,
        "file2.md": """
+line1
-line2
                    """
    }
    expected_checks_dict = {'diff': diff}
    expected_checks = map_checks(expected_checks_dict)
    assert expected_checks.diff == DiffList({
        "file1.md": DiffIndex(
            "file1.md",
            additions={"line1": 2, "line2": 1},
            deletions={"line3": 2, "line4": 1}
        ),
        "file2.md": DiffIndex(
            "file2.md",
            additions={"line1": 1},
            deletions={"line2": 1}
        )
    })
