import pytest
import pyfakefs
import git
import subprocess
import os

from gitjudge.entity import Definition, Repository

def test_givenRepositoryWhithoutArgs_shouldRaiseError():
    with pytest.raises(TypeError):
        Repository()

def test_givenRepositoryWithNonExistentPath_shouldRaiseError():
    with pytest.raises(ValueError):
        Repository("some/non/existent/path")

def test_givenDirectoryThatIsNotAGitRepository_shouldRaiseError(fs):
    with pytest.raises(git.InvalidGitRepositoryError):
        fs.create_dir("existing_non_repository")
        Repository("existing_non_repository")

def test_repositoryShouldHavePath(tmp_path):
    d = tmp_path / "existing_repository"
    d.mkdir()
    os.system(f"git init {d}")

    repository = Repository(d)
    assert repository.directory_path == d
