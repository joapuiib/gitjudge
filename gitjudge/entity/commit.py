from .difflist import DiffList


class Commit:
    def __init__(self, id, message="", branches=[], tags=[], diff=None):
        self.id = id
        self.message = message
        self.hash = ""
        self.committed_date = None

        if diff is None:
            diff = DiffList()
        self.diff = diff

        self.branches = branches
        self.tags = tags
        self.parents = []

    def short_hash(self):
        return self.hash[:7]

    def short_message(self):
        return self.message.split("\n")[0]

    def __str__(self):
        args = []
        args.append(f"id={self.id}")
        if self.hash:
            args.append(f"hash={self.hash}")
        if self.message:
            args.append(f"message={self.message}")
        if self.branches:
            args.append(f"branches={self.branches}")
        if self.tags:
            args.append(f"tags={self.tags}")
        if self.parents:
            args.append(f"parents={self.parents}")
        return f"Commit({', '.join(args)})"

    def __repr__(self):
        return self.__str__()

    # def show_diff(self, colored=True):
    #     print(self.diff(colored=colored))

    # def get_diff(self, colored=False):
    #     if not colored:
    #         ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    #         return ansi_escape.sub('', self.diff)
    #     return self.diff

    def is_cherry_picked_from(self, other_commit):
        """
        Check if this commit is a cherry-pick of the given commit.

        There's no way to know for sure if a commit is a cherry-pick of another,
        but we can make an educated guess by comparing the diff of the two commits.
        If they are the same, then it's very likely that this commit is
        a cherry-pick of the given commit.

        Args:
            commit (Commit): The commit to check if this commit is a cherry-pick of.

        Returns:
            bool: True if this commit is a cherry-pick of the given commit, False otherwise.
        """
        if not other_commit or self.diff.empty():
            return False
        return self.diff == other_commit.diff

    def reverts(self, commit):
        """
        Check if this commit reverts the given commit.

        There's no way to know for sure if a commit reverts another, but we can make
        an educated guess by comparing the diff of the two commits. If the diff of this
        commit contains the diff of the given commit with the signs inverted, then it's
        very likely that this commit reverts the given commit.

        Args:
            commit (Commit): The commit to check if this commit reverts.

        Returns:
            bool: True if this commit reverts the given commit, False otherwise.
        """

        return self.diff == commit.diff.invert()

    def squashes(self, commits):
        """
        Check if this commit squashes the given commits.

        There's no way to know for sure if a commit squashes other commits, but we can make
        an educated guess by merging the diff of the given commits and comparing it to the diff
        of this commit. If they are the same, then it's very likely that this commit squashes
        the given commits.

        Args:
            commits (list): The commits to check if this commit squashes.

        Returns:
            bool: True if this commit squashes the given commits, False otherwise.
        """
        merged_diff = DiffList()
        for commit in commits:
            merged_diff.merge(commit.diff)

        return self.diff == merged_diff

    def get_file_content(self, file):
        with open(file, "r") as f:
            return f.read()


class NotFoundCommit(Commit):
    def __init__(self, id):
        super().__init__(id)

    def __str__(self):
        return f"NotFoundCommit(id={self.id})"

    def __repr__(self):
        return self.__str__()


class ReferencedItselfCommit(Commit):
    def __init__(self, id):
        super().__init__(id)

    def __str__(self):
        return f"ReferencedItselfCommit(id={self.id})"

    def __repr__(self):
        return self.__str__()
