from gitjudge.entity import DiffIndex

class DiffList:

    def __init__(self, diffs=None):
        if diffs is None:
            diffs = {}
        self.diffs = diffs


    def __str__(self):
        args = []
        for diff in self.diffs.values():
            args.append(str(diff))
        return f"DiffList({', '.join(args)})"


    def __repr__(self):
        return str(self)


    def add(self, diffindex):
        self.diffs[diffindex.file_path] = diffindex


    def __eq__(self, other):
        if not isinstance(other, DiffList):
            return False
        return self.diffs == other.diffs


    def empty(self):
        if len(self.diffs) == 0:
            return True

        return all([diff.empty() for diff in self.diffs.values()])


    def clone(self):
        new_diff_list = DiffList()
        new_diff_list.diffs = {k: v.clone() for k, v in self.diffs.items()}
        return new_diff_list


    def merge(self, other):
        for file_path, diff in other.diffs.items():
            if file_path in self.diffs:
                self.diffs[file_path].merge(diff)
            else:
                self.diffs[file_path] = diff.clone()


    def add_addition(self, file_path, line):
        if file_path in self.diffs:
            self.diffs[file_path].add_addition(line)
        else:
            diff = DiffIndex(file_path)
            diff.add_addition(line)
            self.diffs[file_path] = diff


    def add_deletion(self, file_path, line):
        if file_path in self.diffs:
            self.diffs[file_path].add_deletion(line)
        else:
            diff = DiffIndex(file_path)
            diff.add_deletion(line)
            self.diffs[file_path] = diff


    def from_show_output(self, show_output):
        lines = show_output.split("\n")
        file_path = None
        merge = False
        for line in lines:
            if line.startswith("diff --git"):
                file_path = line.split(" ")[-1].replace("b/", "")
                if file_path not in self.diffs:
                    self.diffs[file_path] = DiffIndex(file_path)
                merge = False
            elif line.startswith("diff --cc"):
                file_path = line.split(" ")[-1].replace("b/", "")
                if file_path not in self.diffs:
                    self.diffs[file_path] = DiffIndex(file_path)
                merge = True

            if line.startswith("+++") or line.startswith("---"):
                continue

            if merge:
                if "+" in line[:2]:
                    self.diffs[file_path].add_addition(line[2:])
                elif "-" in line[:2]:
                    self.diffs[file_path].add_deletion(line[2:])
            else:
                if line.startswith("+"):
                    self.diffs[file_path].add_addition(line[1:])
                elif line.startswith("-"):
                    self.diffs[file_path].add_deletion(line[1:])


    def invert(self):
        new = self.clone()
        for diff in new.diffs.values():
            diff.invert()
        return new
