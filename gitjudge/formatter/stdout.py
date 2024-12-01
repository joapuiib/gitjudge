from datetime import datetime

from colorama import Fore, Style

from gitjudge.entity.commit import Commit, NotFoundCommit, ReferencedItselfCommit
from gitjudge.entity.commit_definition import CommitDefinition
from gitjudge.entity.definition import Definition
from gitjudge.entity.repository import Repository


class StdoutFormatter:
    def __init__(self):
        self.checkFormatter = {
            "BranchCheck": self.print_branch_check,
            "CherryPickCheck": self.print_cherry_pick_check,
            "DiffCheck": self.print_diff_check,
            "FileContentCheck": self.print_file_content_check,
            "RevertsCheck": self.print_reverts_check,
            "SquashCheck": self.print_squash_check,
            "TagCheck": self.print_tag_check,
        }

    def print_commit_definition(self, commit_definition: CommitDefinition):
        def print_item(name, value):
            print(f"{name}: {Fore.YELLOW}{value}{Fore.RESET}")

        if commit_definition.start:
            if isinstance(commit_definition.start, NotFoundCommit):
                print_item(
                    "  - Start",
                    f"({commit_definition.start.id}) {Fore.RED}not found{Fore.RESET}",
                )
            elif isinstance(commit_definition.start, Commit):
                print_item(
                    "  - Start",
                    f"({commit_definition.start.id}) {commit_definition.start.short_hash()}",
                )

        if commit_definition.end:
            if isinstance(commit_definition.end, NotFoundCommit):
                print_item(
                    "  - End", f"({commit_definition.end.id}) {Fore.RED}not found{Fore.RESET}"
                )
            elif isinstance(commit_definition.end, Commit):
                print_item(
                    "  - End", f"({commit_definition.end.id}) {commit_definition.end.short_hash()}"
                )

        if commit_definition.message:
            print_item("  - Message", commit_definition.message)
        if commit_definition.tags:
            print_item("  - Tags", commit_definition.tags)
        if commit_definition.branches:
            print_item("  - Branches", commit_definition.branches)

    def print_not_found_commit(self, not_found_commit: NotFoundCommit):
        print(f"{Fore.RED}Commit {not_found_commit.id} not found{Fore.RESET}")

    def print_commit(
        self,
        definition: Definition,
        commit_definition: CommitDefinition,
        commit: Commit,
        repo: Repository,
    ):
        if not isinstance(commit_definition, CommitDefinition):
            raise ValueError("StdoutFormmater: commit_definition must be a CommitDefinition object")
        if not isinstance(commit, Commit):
            raise ValueError("StdoutFormmater: commit must be a Commit object")
        if not isinstance(repo, Repository):
            raise ValueError("StdoutFormmater: repo must be a Repository object")

        correct = commit_definition.is_correct
        limit_date = definition.limit_date

        short_hash = commit.short_hash()
        message = commit.short_message()
        commit_date = commit.committed_date

        # color_title = Fore.GREEN if correct else Fore.RED
        color_title = Fore.WHITE
        print(
            f"==== {Style.BRIGHT}{Fore.BLUE}{short_hash}{Fore.RESET} - {color_title}{message}{Fore.RESET}{Style.RESET_ALL} ====",
            end=" ",
        )

        if correct:
            print(f"{Fore.GREEN}OK!{Fore.RESET}")
        else:
            print(f"{Fore.RED}ERROR!{Fore.RESET}")
            # print_commit_details(commit)

        if limit_date:
            limit_date = datetime.fromisoformat(limit_date)
            seconds_since_epoch = commit.committed_date
            commit_date = datetime.fromtimestamp(seconds_since_epoch)
            print(f"Limit date: {limit_date}")
            print(f"Last change: {commit_date}")
            if commit_date > limit_date:
                print(
                    Fore.RED
                    + "COMPTE!! El tag ha segut modificat després de la data d'entrega"
                    + Fore.RESET
                )

        for check in commit_definition.checks:
            self.print_check(check, commit, repo)

    def print_check(self, check, commit, repo):
        f = self.checkFormatter.get(type(check).__name__, self.print_check_fallback)
        f(check, commit, repo)

    def print_check_fallback(self, check, commit, repo):
        result = f"{Fore.GREEN}YES{Fore.RESET}" if check.correct else f"{Fore.RED}NO{Fore.RESET}"
        print(f"  - {check}: {result}")

    def print_branch_check(self, check, commmit, repo):
        for branch, correct in check.branches.items():
            result = f"{Fore.GREEN}YES{Fore.RESET}" if correct else f"{Fore.RED}NO{Fore.RESET}"
            print(f"  - Has {Fore.YELLOW}'{branch}'{Fore.RESET} branch? {result}")

    def print_cherry_pick_check(self, check, commit, repo):
        if isinstance(check.reference, NotFoundCommit):
            print(
                f"- Cherry-picked from commit ({check.reference.id}) {Fore.RED}not found{Fore.RESET}."
            )
        elif isinstance(check.reference, ReferencedItselfCommit):
            print(f"- Cherry-picked from commit {Fore.RED}can't reference itself{Fore.RESET}.")
        else:
            result = (
                f"{Fore.GREEN}YES{Fore.RESET}" if check.correct else f"{Fore.RED}NO{Fore.RESET}"
            )
            _id = check.reference.id
            _hash = check.reference.short_hash()
            print(f"- Is cherry-picked from {Fore.YELLOW}'({_id}) {_hash}'{Fore.RESET}? {result}")

    def print_diff_check(self, check, commit, repo):
        diff_correct = check.correct
        diff_result = (
            f"{Fore.GREEN}YES{Fore.RESET}" if diff_correct else f"{Fore.RED}NO{Fore.RESET}"
        )
        print(f"  - Is diff correct? {diff_result}")
        if not diff_correct:
            print(f"      {Fore.YELLOW}Expected diff:{Fore.RESET}")
            for file, diff_index in check.diff.items():
                print(f"      {Fore.CYAN}- {file}{Fore.RESET}")
                if diff_index.additions:
                    for line, count in diff_index.additions.items():
                        print(f"        {count}+: {line}")
                if diff_index.deletions:
                    for line, count in diff_index.deletions.items():
                        print(f"        {count}-: {line}")

            print(f"      {Fore.YELLOW}Actual diff:{Fore.RESET}")
            for file, diff_index in commit.diff.items():
                print(f"      {Fore.CYAN}- {file}{Fore.RESET}")
                if diff_index.additions:
                    for line, count in diff_index.additions.items():
                        print(f"        {count}+: {line}")
                if diff_index.deletions:
                    for line, count in diff_index.deletions.items():
                        print(f"        {count}-: {line}")

    def print_file_content_check(self, check, commit, repo):
        file_content_correct = check.correct
        result = (
            f"{Fore.GREEN}YES{Fore.RESET}" if file_content_correct else f"{Fore.RED}NO{Fore.RESET}"
        )
        for file, correct in check.results.items():
            result = f"{Fore.GREEN}YES{Fore.RESET}" if correct else f"{Fore.RED}NO{Fore.RESET}"
            print(f"  - Is {Fore.YELLOW}'{file}'{Fore.RESET} content correct? {result}")
            if not correct:
                print(f"    {Fore.YELLOW}Expected content:{Fore.RESET}")
                expected_content = check.file_contents[file]
                expected_content = check.strip_lines(expected_content)
                expected_content = "\n".join(
                    [f"      {line}" for line in expected_content.split("\n")]
                )
                print(f"{expected_content}")
                print(f"    {Fore.YELLOW}Actual content:{Fore.RESET}")
                actual_content = repo.get_file_content_from_ref(file, commit.hash)
                actual_content = check.strip_lines(actual_content)
                actual_content = "\n".join([f"      {line}" for line in actual_content.split("\n")])
                print(f"{actual_content}")

    def print_reverts_check(self, check, commit, repo):
        if isinstance(check.reference, NotFoundCommit):
            print(f"- Reverting commit ({check.reference.id}) {Fore.RED}not found{Fore.RESET}.")
        elif isinstance(check.reference, ReferencedItselfCommit):
            print(f"- Reverting commit {Fore.RED}can't reference itself{Fore.RESET}.")
        else:
            result = (
                f"{Fore.GREEN}YES{Fore.RESET}" if check.correct else f"{Fore.RED}NO{Fore.RESET}"
            )
            _id = check.reference.id
            _hash = check.reference.short_hash()
            print(f"- Reverts {Fore.YELLOW}'({_id}) {_hash}'{Fore.RESET}? {result}")

    def print_squash_check(self, check, commit, repo):
        squash_result = (
            f"{Fore.GREEN}YES{Fore.RESET}" if check.correct else f"{Fore.RED}NO{Fore.RESET}"
        )
        squash_output = ", ".join([f"{commit.short_hash()}" for commit in check.references])
        print(f"- Does squash {Fore.YELLOW}'{squash_output}'{Fore.RESET}? {squash_result}")

    def print_tag_check(self, check, commit, repo):
        for tag, correct in check.tags.items():
            result = f"{Fore.GREEN}YES{Fore.RESET}" if correct else f"{Fore.RED}NO{Fore.RESET}"
            print(f"- Has {Fore.YELLOW}'{tag}'{Fore.RESET} tag? {result}")

    def print_log(self, definition: Definition, repo: Repository):
        first_commit = None
        last_commit = None
        for cd in definition.commits:
            if cd.commit:
                if not first_commit or cd.commit.id < first_commit.id:
                    first_commit = cd.commit
                if not last_commit or cd.commit.id > last_commit.id:
                    last_commit = cd.commit

        print()
        print(f"==== {Fore.BLUE}{Style.BRIGHT}Repository log{Style.RESET_ALL}{Fore.RESET} ====")
        repo.print_log(
            start=first_commit,
            end=last_commit,
            branches=definition.log_options.branches,
            all=definition.log_options.all,
        )
