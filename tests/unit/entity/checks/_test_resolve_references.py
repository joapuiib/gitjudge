from gitjudge.entity import (
    Checks,
    CommitDefinition,
)


def testResolveReferences_givenNothing_expectNoChange(validator):
    expected = CommitDefinition("id")
    validator.resolve_references_checks(expected)

    assert expected.start == None
    assert expected.end == None
    assert expected.checks == None


# TODO
def testResolveReferences_givenSquashesByBranch_expectListOfCommits(validator):
    expected = CommitDefinition("id")
    expected.checks = Checks()
    expected.checks.squashes = "squash-branch"
    commit = validator.repo.find_commit_by_ref("Squashed")
    validator.resolve_references_checks(expected, commit)

    assert len(expected.checks.squashes) == 2
    assert expected.checks.squashes[0].message == "5. first change to file1.md"
    assert expected.checks.squashes[1].message == "6. second change to file1.md"
