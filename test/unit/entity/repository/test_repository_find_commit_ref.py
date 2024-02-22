import pytest

from gitjudge.entity import Repository, Commit

def testFindByRef_givenEmptyRepo_expectNotFound(empty_repo):
    repo = empty_repo
    commit = repo.find_commit_by_ref("main")

    assert commit is Commit.NotFoundCommit

def testFindByRef_givenInexistentRef_expectNotFound(repo):
    commit = repo.find_commit_by_ref("inexistent")

    assert commit is Commit.NotFoundCommit

def testFindByRef_givenRef_expectCommit(repo):
    commit = repo.find_commit_by_ref("main")

    assert isinstance(commit, Commit)
    assert commit.hash is not None
