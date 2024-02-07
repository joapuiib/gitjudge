from datetime import datetime

class Definition:
    def __init__(self, name: str):
        self.name = name
        self.limit_date = None
        self.expected_commits = []
