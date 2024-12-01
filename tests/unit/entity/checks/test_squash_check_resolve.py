from gitjudge.entity.checks import SquashCheck
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
| * 646b91a - (0 seconds ago) 9. Squashed changes to file1.md - Joan Puigcerver (squashed, tag: squashed)
|/
* 7cb78bd - (0 seconds ago) 2. modified file1.md - Joan Puigcerver (HEAD -> main, tag: T3, tag: T2)
* 27f0b5f - (0 seconds ago) 1. added file1.md - Joan Puigcerver (tag: T1)
"""


def test_givenCommitIds_shouldResolveReference(found_commits, resolver):
    references = [7, 8]
    check = SquashCheck(references)
    check.resolve_references(9, resolver)

    assert check.references == [found_commits[7], found_commits[8]]


def test_givenCommitRefs_shouldResolveReference(found_commits, resolver):
    references = ["branch1", "branch2"]
    check = SquashCheck(references)
    check.resolve_references(9, resolver)

    assert len(check.references) == 2
    assert check.references[0].id == "branch1"
    assert check.references[1].id == "branch2"


def test_givenSameCommitId_shouldResolveReferencedItself(found_commits, resolver):
    references = [7, 8]
    check = SquashCheck(references)
    check.resolve_references(7, resolver)

    assert isinstance(check.references[0], ReferencedItselfCommit)


def test_givenNonExistingCommitId_shouldResolveNotFound(found_commits, resolver):
    references = [-1, -2]
    check = SquashCheck(references)
    check.resolve_references(9, resolver)

    assert isinstance(check.references[0], NotFoundCommit)
    assert isinstance(check.references[1], NotFoundCommit)
