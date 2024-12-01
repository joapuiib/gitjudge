from gitjudge.entity.checks import BranchCheck

"""
* c5bf0d3 - (0 seconds ago) 3. added branch1.md - Joan Puigcerver (branch1)
| * 57b1900 - (0 seconds ago) 4. added branch2.md - Joan Puigcerver (branch2.2, branch2)
|/
| * 6dbc914 - (0 seconds ago) 6. Cherry-pick "2. modified file1.md" - Joan Puigcerver (revert-cherry)
| * ebf5774 - (0 seconds ago) 5. Revert "2. modified file1.md" - Joan Puigcerver
|/
| * f533136 - (0 seconds ago) 8. second change squash - Joan Puigcerver (squash-branch)
| * a692df0 - (0 seconds ago) 7. first change squash - Joan Puigcerver
|/
| * 646b91a - (0 seconds ago) 9. Squashed changes to file1.md - Joan Puigcerver (tag: squashed, squashed)
|/
* 7cb78bd - (0 seconds ago) 2. modified file1.md - Joan Puigcerver (HEAD -> main, tag: T3, tag: T2)
* 27f0b5f - (0 seconds ago) 1. added file1.md - Joan Puigcerver (tag: T1)
"""
repo = None


def test_hasSingleBranch_shouldBeCorrect(found_commits):
    check = BranchCheck(["main"])
    commit = found_commits[2]
    correct = check.validate(commit, repo)

    assert correct
    assert check.correct
    assert check.branches == {"main": True}


def test_notHasSingleBranch_shouldBeIncorrect(found_commits):
    check = BranchCheck(["main"])
    commit = found_commits[1]

    correct = check.validate(commit, repo)
    assert not correct
    assert not check.correct
    assert check.branches == {"main": False}


def test_hasAllBranches_shouldBeCorrect(found_commits):
    check = BranchCheck(["branch2", "branch2.2"])
    commit = found_commits[4]

    correct = check.validate(commit, repo)
    assert correct
    assert check.correct
    assert check.branches == {"branch2": True, "branch2.2": True}


def test_hasSomeBranches_shouldBeIncorrect(found_commits):
    check = BranchCheck(["branch1", "main"])
    commit = found_commits[3]

    correct = check.validate(commit, repo)
    assert not correct
    assert not check.correct
    assert check.branches == {"branch1": True, "main": False}
