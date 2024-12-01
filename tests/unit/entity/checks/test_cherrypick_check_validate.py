from gitjudge.entity.checks import CherryPickCheck
from gitjudge.entity.commit import NotFoundCommit, ReferencedItselfCommit


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


def test_givenCherryPickedCommit_shouldBeCorrect(found_commits):
    # Commit 6 is a cherry-pick of Commit 2
    check = CherryPickCheck(found_commits[2])
    commit = found_commits[6]

    correct = check.validate(commit, repo)
    assert correct
    assert check.correct


def test_givenNotCherryPickedCommit_shouldBeNotCorrect(found_commits):
    # Commit 6 is a cherry-pick of Commit 1
    check = CherryPickCheck(found_commits[1])
    commit = found_commits[6]

    correct = check.validate(commit, repo)
    assert not correct
    assert not check.correct


def test_givenNotFoundCommit_shouldBeNotCorrect(found_commits):
    check = CherryPickCheck(NotFoundCommit(1))
    commit = found_commits[6]

    correct = check.validate(commit, repo)
    assert not correct
    assert not check.correct


def test_givenReferencedItselfCommit_shouldBeNotCorrect(found_commits):
    check = CherryPickCheck(ReferencedItselfCommit(1))
    commit = found_commits[6]

    correct = check.validate(commit, repo)
    assert not correct
    assert not check.correct
