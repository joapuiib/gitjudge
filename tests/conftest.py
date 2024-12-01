import pytest
import os
from pathlib import Path
from argparse import Namespace

from gitjudge.entity.commit import Commit
from gitjudge.entity.commit_definition import CommitDefinition
from gitjudge.entity.definition import Definition
from gitjudge.entity.difflist import DiffList
from gitjudge.entity.diffindex import DiffIndex
from gitjudge.entity.reference_resolver import ReferenceResolver
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
    d = tmpdir_factory.mktemp("repository")
    os.system(f"git init {d}")
    repo = Repository(d)

    Path.touch(repo.directory_path / "file1.md")
    with open(repo.directory_path / "file1.md", "a") as f:
        f.write("1\n")
    repo.repo.git.add("--all")
    repo.repo.git.commit(m="1. added file1.md")
    repo.repo.git.tag("T1")

    repo.repo.git.branch("-m", "main")

    with open(repo.directory_path / "file1.md", "a") as f:
        f.write("2\n")
    repo.repo.git.add("--all")
    repo.repo.git.commit(m="2. modified file1.md")
    repo.repo.git.tag("T2")
    repo.repo.git.tag("T3")

    repo.repo.git.checkout("-b", "branch1")
    Path.touch(repo.directory_path / "branch1.md")
    with open(repo.directory_path / "branch1.md", "a") as f:
        f.write("3\n")
    repo.repo.git.add("--all")
    repo.repo.git.commit(m="3. added branch1.md")

    repo.repo.git.checkout("main")
    repo.repo.git.checkout("-b", "branch2")
    Path.touch(repo.directory_path / "branch2.md")
    with open(repo.directory_path / "branch1.md", "a") as f:
        f.write("4\n")
    repo.repo.git.add("--all")
    repo.repo.git.commit(m="4. added branch2.md")
    repo.repo.git.branch("branch2.2")

    repo.repo.git.checkout("main")
    repo.repo.git.checkout("-b", "revert-cherry")
    repo.repo.git.revert("main", no_commit=True)
    repo.repo.git.commit(m='5. Revert "2. modified file1.md"')
    repo.repo.git.cherry_pick("main", no_commit=True)
    repo.repo.git.commit(m='6. Cherry-pick "2. modified file1.md"')

    repo.repo.git.checkout("main")
    repo.repo.git.checkout("-b", "squash-branch")
    with open(repo.directory_path / "file1.md", "a") as f:
        f.write("7")
    repo.repo.git.add("--all")
    repo.repo.git.commit(m="7. first change squash")

    with open(repo.directory_path / "file1.md", "a") as f:
        f.write("8")
    repo.repo.git.add("--all")
    repo.repo.git.commit(m="8. second change squash")

    repo.repo.git.checkout("main")
    repo.repo.git.checkout("-b", "squashed")
    repo.repo.git.merge("--squash", "squash-branch")
    repo.repo.git.commit(m="9. Squashed changes to file1.md")
    repo.repo.git.tag("squashed")

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
            diff=DiffList({"file1.md": DiffIndex("file1.md", additions={"1": 1})}),
        ),
        2: Commit(
            2,
            message="2. modified file1.md",
            tags=["T2", "T3"],
            branches=["main"],
            diff=DiffList({"file1.md": DiffIndex("file1.md", additions={"2": 1})}),
        ),
        3: Commit(
            3,
            message="Added branch1.md",
            branches=["branch1"],
            diff=DiffList({"branch1.md": DiffIndex("branch1.md", deletions={"3": 1})}),
        ),
        4: Commit(
            4,
            message="Added branch2.md",
            branches=["branch2", "branch2.2"],
            diff=DiffList({"branch2.md": DiffIndex("branch2.md", additions={"4": 1})}),
        ),
        5: Commit(
            5,
            message='5. Revert "2. modified file1.md"',
            diff=DiffList({"file1.md": DiffIndex("file1.md", deletions={"2": 1})}),
        ),
        6: Commit(
            6,
            message='6. Cherry-pick "2. modified file1.md"',
            diff=DiffList({"file1.md": DiffIndex("file1.md", additions={"2": 1})}),
        ),
        7: Commit(
            7,
            message="7. first change squash",
            diff=DiffList({"file1.md": DiffIndex("file1.md", additions={"7": 1})}),
        ),
        8: Commit(
            8,
            message="8. second change squash",
            branches=["squash-branch"],
            diff=DiffList({"file1.md": DiffIndex("file1.md", additions={"8": 1})}),
        ),
        9: Commit(
            9,
            message="9. Squashed changes to file1.md",
            branches=["squashed"],
            tags=["squashed"],
            diff=DiffList({"file1.md": DiffIndex("file1.md", additions={"7": 1, "8": 1})}),
        ),
    }


@pytest.fixture
def validator(found_commits, definition, repo):
    args = Namespace(show=False)
    formatter = None
    validator = Validator(args, definition, repo, formatter)
    validator.resolver.found_commits = found_commits
    return validator


@pytest.fixture
def resolver(found_commits, repo):
    return ReferenceResolver(repo, found_commits)
