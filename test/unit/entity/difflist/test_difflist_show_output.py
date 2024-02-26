import pytest

from gitjudge.entity import DiffList, DiffIndex

def test_create_diff_with_addition_and_deletion():
    diff = """\
diff --git a/file.md b/file.md
index f63f268..4afe310 100644
--- a/file.md
+++ b/file.md
@@ -3,3 +3,4 @@
 ## Un
-Del
-Del
+Add
"""

    difflist = DiffList()
    difflist.from_show_output(diff)

    assert len(difflist.diffs) == 1
    assert "file.md" in difflist.diffs
    assert difflist.diffs["file.md"].file_path == "file.md"
    assert difflist.diffs["file.md"].additions == {"Add": 1}
    assert difflist.diffs["file.md"].deletions == {"Del": 2}

def test_create_diff_with_addition_and_deletion_merge_commit():
    diff = """\
diff --cc file.md
index f63f268,4afe310..4afe310
--- a/file.md
+++ b/file.md
@@@ -3,3 -3,4 +3,4 @@@
  ## Un
 -Del
- Del
+ Add
 +Add
"""

    difflist = DiffList()
    difflist.from_show_output(diff)

    assert len(difflist.diffs) == 1
    assert "file.md" in difflist.diffs
    assert difflist.diffs["file.md"].file_path == "file.md"
    assert difflist.diffs["file.md"].additions == {"Add": 2}
    assert difflist.diffs["file.md"].deletions == {"Del": 2}

def test_create_diff_with_multiple_files():
    diff = """\
diff --git a/file.md b/file.md
index f63f268..4afe310 100644
--- a/file.md
+++ b/file.md
@@ -3,3 +3,4 @@
 ## Un
-Del
+Add

diff --cc b/file2.md
index f63f268..4afe310 100644
--- a/file2.md
+++ b/file2.md
@@@ -3,3 +3,4 @@
 ## Un
- Del
 -Del
+ Add
 +Add
"""

    difflist = DiffList()
    difflist.from_show_output(diff)

    assert len(difflist.diffs) == 2
    assert "file.md" in difflist.diffs
    assert "file2.md" in difflist.diffs
    assert difflist.diffs["file.md"].file_path == "file.md"
    assert difflist.diffs["file.md"].additions == {"Add": 1}
    assert difflist.diffs["file.md"].deletions == {"Del": 1}
    assert difflist.diffs["file2.md"].file_path == "file2.md"
    assert difflist.diffs["file2.md"].additions == {"Add": 2}
    assert difflist.diffs["file2.md"].deletions == {"Del": 2}


def test_create_diff_commit_info():
    diff = """\
commit f6aca2d2b135a47cb3a4064075490267b2d16250
Author: Joan Puigcerver <joapuiib@gmail.com>
Date:   Mon Feb 26 11:20:23 2024 +0100

    2. added title to file1.md

diff --git a/file1.md b/file1.md
index e69de29..ccd0f29 100644
--- a/file1.md
+++ b/file1.md
@@ -0,0 +1 @@
+# Populated repo
"""

    difflist = DiffList()
    difflist.from_show_output(diff)

    assert len(difflist.diffs) == 1
    assert "file1.md" in difflist.diffs
    assert difflist.diffs["file1.md"].file_path == "file1.md"
    assert difflist.diffs["file1.md"].additions == {"# Populated repo": 1}
    assert difflist.diffs["file1.md"].deletions == {}

