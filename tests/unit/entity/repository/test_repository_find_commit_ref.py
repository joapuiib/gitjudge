from gitjudge.entity.commit import Commit, NotFoundCommit


def testFindByRef_givenEmptyRepo_expectNotFound(empty_repo):
    repo = empty_repo
    commit = repo.find_commit_by_ref("main")

    assert isinstance(commit, NotFoundCommit)
    assert commit.id == "main"


def testFindByRef_givenInexistentRef_expectNotFound(repo):
    commit = repo.find_commit_by_ref("inexistent")

    assert isinstance(commit, NotFoundCommit)
    assert commit.id == "inexistent"


def testFindByRef_givenRef_expectCommit(repo):
    commit = repo.find_commit_by_ref("main")

    assert isinstance(commit, Commit)
    assert commit.hash is not None
