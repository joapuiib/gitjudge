from gitjudge.entity.checks import SquashCheck


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


def test_givenSquashedCommits_shouldBeCorrect(found_commits):
    # Commit 9 is squashed from commits 7 and 8
    squash_commits = [found_commits[7], found_commits[8]]
    check = SquashCheck(squash_commits)
    commit = found_commits[9]

    correct = check.validate(commit, repo)
    assert correct
    assert check.correct


def test_givenNonSquashedCommits_shouldNotBeCorrect(found_commits):
    # Commit 9 is squashed from commits 7 and 8
    squash_commits = [found_commits[7], found_commits[8]]
    check = SquashCheck(squash_commits)
    commit = found_commits[1]

    correct = check.validate(commit, repo)
    assert not correct
    assert not check.correct
