from gitjudge.entity.commit import Commit, NotFoundCommit, ReferencedItselfCommit
from gitjudge.entity.reference_resolver import ReferenceResolver


def test_constructor():
    resolver = ReferenceResolver(repo=None)

    assert resolver.references == {}


def test_givenExistingReference_shouldResolveReference(found_commits):
    resolver = ReferenceResolver(repo=None, references=found_commits)

    commit = resolver.resolve_reference(commit_id=None, reference=1)

    assert isinstance(commit, Commit)
    assert commit == found_commits[1]


def test_givenSameReferenceAndId_shouldResolveReferencedItself(found_commits):
    resolver = ReferenceResolver(repo=None, references=found_commits)

    commit = resolver.resolve_reference(commit_id=1, reference=1)

    assert isinstance(commit, ReferencedItselfCommit)


def test_givenNotFoundReference_shouldReturnNotFoundCommit(found_commits):
    resolver = ReferenceResolver(repo=None, references=found_commits)

    commit = resolver.resolve_reference(commit_id=None, reference=-1)

    assert isinstance(commit, NotFoundCommit)


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


def test_givenReferenceAsString_shouldResolveReferenceFromRepo(repo):
    resolver = ReferenceResolver(repo=repo)

    commit = resolver.resolve_reference(commit_id=None, reference="main")

    assert isinstance(commit, Commit)
    assert commit.id == "main"
