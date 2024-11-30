import pytest
import os
from pathlib import Path
from argparse import Namespace

from gitjudge.entity.commit import Commit
from gitjudge.entity.commit_definition import CommitDefinition
from gitjudge.entity.definition import Definition
from gitjudge.entity.difflist import DiffList
from gitjudge.entity.diffindex import DiffIndex
from gitjudge.entity.repository import Repository
from gitjudge.entity.validator import Validator

@pytest.fixture(scope="session")
def empty_repo(tmpdir_factory):
    d = tmpdir_factory.mktemp("empty-repository")
    os.system(f"git init {d}")
    return Repository(d)

@pytest.fixture(scope="session")
def repo(tmpdir_factory):
    """
    * ae33661 - (0 seconds ago) 3. added branch1.md - Joan Puigcerver (branch1)
    | * 058a064 - (0 seconds ago) 4. added branch2.md - Joan Puigcerver (branch2)
    |/
    * 8ba96a6 - (0 seconds ago) 2. modified file1.md - Joan Puigcerver (HEAD -> main, tag: T3, tag: T2)
    * 1ebb397 - (0 seconds ago) 1. added file1.md - Joan Puigcerver (tag: T1)
    """
    d = tmpdir_factory.mktemp("repository")
    os.system(f"git init {d}")
    repo = Repository(d)

    Path.touch(repo.directory_path / "file1.md")
    repo.repo.git.add('--all')
    repo.repo.git.commit(m="1. added file1.md")
    repo.repo.git.tag("T1")

    repo.repo.git.branch("-m", "main")

    with open(repo.directory_path / "file1.md", "a") as f:
        f.write("# Populated repo\n")
    repo.repo.git.add('--all')
    repo.repo.git.commit(m="2. added title to file1.md")
    repo.repo.git.tag("T2")
    repo.repo.git.tag("T3")

    repo.repo.git.checkout("-b", "branch1")
    Path.touch(repo.directory_path / "branch1.md")
    repo.repo.git.add('--all')
    repo.repo.git.commit(m="3. added branch1.md")

    repo.repo.git.checkout("main")
    repo.repo.git.checkout("-b", "branch2")
    Path.touch(repo.directory_path / "branch2.md")
    repo.repo.git.add('--all')
    repo.repo.git.commit(m="4. added branch2.md")

    repo.repo.git.checkout("main")
    repo.repo.git.checkout("-b", "squash-branch")
    with open(repo.directory_path / "file1.md", "a") as f:
        f.write("- first change to file1.md\n")
    repo.repo.git.add('--all')
    repo.repo.git.commit(m="5. first change to file1.md")

    with open(repo.directory_path / "file1.md", "a") as f:
        f.write("- second change to file1.md\n")
    repo.repo.git.add('--all')
    repo.repo.git.commit(m="6. second change to file1.md")

    repo.repo.git.checkout("main")
    repo.repo.git.merge("--squash", "squash-branch")
    repo.repo.git.commit(m="7. Squashed changes to file1.md")
    repo.repo.git.tag("Squashed")

    repo.repo.git.checkout("main")
    return repo

@pytest.fixture()
def definition():
    definition = Definition("test-definition")
    definition.expected_commits = [
        CommitDefinition(id="1", message="1."),
        CommitDefinition(id="2", message="2."),
        CommitDefinition(id="3", message="3.", start="branch1"),
    ]
    return definition

@pytest.fixture
def found_commits():
    return {
        1: Commit(
            1,
            message="1. added file1.md",
            tags=["T1"],
            diff=DiffList({
                "file1.md": DiffIndex(
                    "file1.md",
                    additions={"1": 1}
                )
            })
        ),
        2: Commit(
            2,
            message="2. modified file1.md",
            tags=["T2", "T3"],
            diff=DiffList({
                "file1.md": DiffIndex(
                    "file1.md",
                    additions={"2": 1}
                )
            })
        ),
        3: Commit(
            3,
            message="Revert \"Commit 2\"",
            diff=DiffList({
                "file1.md": DiffIndex(
                    "file1.md",
                    deletions={"2": 1}
                )
            })
        ),
        4: Commit(
            4,
            message="Cherry-pick \"Commit 1\"",
            diff=DiffList({
                "file1.md": DiffIndex(
                    "file1.md",
                    additions={"1": 1}
                )
            })
        ),
    }


@pytest.fixture
def validator(found_commits, definition, repo):
    args = Namespace(show=False)
    formatter = None
    validator = Validator(args, definition, repo, formatter)
    validator.resolver.found_commits = found_commits
    return validator
