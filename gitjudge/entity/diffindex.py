class DiffIndex:
    """
    A simplified representation of a diff from a git.Diff object.

    It is used to perform simplified diff operations.

    It contains two dicts to store the time each addition or deletion
    is present in a file.
    """

    def __init__(self, file_path, additions=None, deletions=None):
        self.file_path = file_path

        if additions is None:
            additions = {}
        self.additions = additions

        if deletions is None:
            deletions = {}
        self.deletions = deletions


    def __str__(self):
        args = []
        args.append(f"file_path={self.file_path}")
        if self.additions:
            additions = (f"additions=")
            additions += ", ".join([f"{times}+: {line}" for line, times in self.additions.items()])
            args.append(additions)
        if self.deletions:
            deletions = (f"deletions=")
            deletions += ", ".join([f"{times}-: {line}" for line, times in self.deletions.items()])
            args.append(deletions)
        return f"DiffIndex({', '.join(args)})"


    def __repr__(self):
        return str(self)


    def empty(self):
        """
        Return True if the diff is empty, False otherwise.
        """

        return len(self.additions) == 0 and len(self.deletions) == 0


    def add_addition(self, line):
        """
        Increase the times a line is added to a file by one.

        If the line is deleted, it is removed from the deletions dict.
        """

        if line in self.deletions:
            delete_time = self.deletions[line]
            if delete_time > 1:
                self.deletions[line] -= 1
            else:
                del self.deletions[line]
        else:
            if line in self.additions:
                self.additions[line] += 1
            else:
                self.additions[line] = 1

    def add_deletion(self, line):
        """
        Increase the times a line is deleted from a file by one.

        If the line is added, it is removed from the additions dict.
        """

        if line in self.additions:
            addition_time = self.additions[line]
            if addition_time > 1:
                self.additions[line] -= 1
            else:
                del self.additions[line]
        else:
            if line in self.deletions:
                self.deletions[line] += 1
            else:
                self.deletions[line] = 1

    def __eq__(self, other):
        same_file = self.file_path == other.file_path
        same_additions = self.additions == other.additions
        same_deletions = self.deletions == other.deletions
        return same_file and same_additions and same_deletions


    def clone(self):
        """
        Return a new DiffIndex with the same file_path, additions and deletions.
        """

        new_diff_index = DiffIndex(self.file_path)
        new_diff_index.additions = self.additions.copy()
        new_diff_index.deletions = self.deletions.copy()
        return new_diff_index


    def merge(self, other):
        """
        Merge the additions and deletions of another DiffIndex into this one.
        """
        for line, times in other.additions.items():
            for _ in range(times):
                self.add_addition(line)

        for line, times in other.deletions.items():
            for _ in range(times):
                self.add_deletion(line)


    def invert(self):
        """
        Invert the additions and deletions of this DiffIndex.
        """
        aux = self.additions
        self.additions = self.deletions
        self.deletions = aux
