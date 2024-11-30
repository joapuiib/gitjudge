from gitjudge.entity.commit import Commit, NotFoundCommit, ReferencedItselfCommit

from .check import Check


class FileContentCheck(Check):
    def __init__(self, file_contents: dict):
        self.file_contents = file_contents
        self.results = {}
        for file_path in self.file_contents.keys():
            self.results[file_path] = False


    def __str__(self):
        return f"FileContentCheck({self.file_contents})"


    def __repr__(self):
        return self.__str__()


    def validate(self, commit, repo) -> bool:
        super().validate(commit, repo)

        if isinstance(commit, NotFoundCommit) or isinstance(commit, ReferencedItselfCommit):
            self.correct = False
            return self.correct

        for file_path, file_content in self.file_contents.items():
            file_content = self.strip_lines(file_content)

            revision_contents = repo.get_file_content_from_ref(file_path, commit.hash)
            revision_contents = self.strip_lines(revision_contents)

            self.results[file_path] = file_content in revision_contents
            self.correct = self.correct and self.results[file_path]

        return self.correct


    def strip_lines(self, content: str) -> str:
        return "\n".join([line.strip() for line in content.split("\n") if line.strip()])
