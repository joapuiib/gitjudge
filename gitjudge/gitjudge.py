#!/usr/bin/env python3.8
import argparse

from gitjudge.entity.repository import Repository
from gitjudge.entity.validator import Validator
from gitjudge.formatter import StdoutFormatter
from gitjudge.mapper.definition import load_definition


class GitJudge:
    def __init__(self, args):
        self.args = args
        self.definition = load_definition(args.definition_file)
        self.formatter = StdoutFormatter()

    def validate(self, repo_dir):
        repo = Repository(repo_dir)
        validator = Validator(self.args, self.definition, repo, self.formatter)
        validator.validate()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("definition_file", help="Path to the definition file.")
    parser.add_argument("dir", nargs="+", help="Git Directory to validate.")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    gitjudge = GitJudge(args)
    for repo_dir in args.dir:
        gitjudge.validate(repo_dir)


if __name__ == "__main__":
    main()
