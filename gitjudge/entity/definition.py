from datetime import datetime

from gitjudge.entity import LogOptions

class Definition:
    def __init__(self, name: str):
        self.name = name
        self.limit_date = None
        self.expected_commits = []

        self.log_options = LogOptions()

    def __str__(self):
        args = []

        args.append(f"name={self.name}")
        if self.limit_date:
            args.append(f"limit_date={self.limit_date}")
        if self.expected_commits:
            args.append(f"expected_commits={self.expected_commits}")
        if self.log_options:
            args.append(f"log_options={self.log_options}")
        return f"Definition({', '.join(args)})"

    def __repr__(self):
        return self.__str__()
