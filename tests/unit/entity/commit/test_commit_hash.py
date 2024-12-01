from gitjudge.entity.commit import Commit


def test_giventCommitWithNohash_thenEmptyHashIsReturned():
    commit = Commit(1)
    assert commit.short_hash() == ""


def test_givenCommitWithHash_thenShortHashIsReturned():
    commit = Commit(1)
    commit.hash = "1234567890"
    assert commit.short_hash() == "1234567"
