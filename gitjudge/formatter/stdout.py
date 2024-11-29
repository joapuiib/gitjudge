from colorama import Fore, Style

from gitjudge.entity import Commit, CommitDefinition, CheckResult, NotFoundCommit, ReferencedItselfCommit, Definition

class StdoutFormatter:
    def __init__(self):
        self.checkFormatter = {
            "BranchCheck": self.print_branch_check,
            "CherryPickCheck": None,
            "DiffCheck": self.print_diff_check,
            "RevertsCheck": None,
            "SquashCheck": None,
            "TagCheck": self.print_tag_check,
        }

    def print_commit_definition(self, commit_definition: CommitDefinition):
        def print_item(name, value):
            print(f"{name}: {Fore.YELLOW}{value}{Fore.RESET}")

        if commit_definition.start:
            if isinstance(commit_definition.start, NotFoundCommit):
                print_item(f"  - Start", f"({commit_definition.start.id}) {Fore.RED}not found{Fore.RESET}")
            elif isinstance(commit_definition.start, Commit):
                print_item(f"  - Start", f"({commit_definition.start.id}) {commit_definition.start.short_hash()}")

        if commit_definition.end:
            if isinstance(commit_definition.end, NotFoundCommit):
                print_item(f"  - End", f"({commit_definition.end.id}) {Fore.RED}not found{Fore.RESET}")
            elif isinstance(commit_definition.end, Commit):
                print_item(f"  - End", f"({commit_definition.end.id}) {commit_definition.end.short_hash()}")

        if commit_definition.message:
            print_item("  - Message", commit_definition.message)
        if commit_definition.tags:
            print_item("  - Tags", commit_definition.tags)
        if commit_definition.branches:
            print_item("  - Branches", commit_definition.branches)


    def print_not_found_commit(self, not_found_commit: NotFoundCommit):
        print(f"{Fore.RED}Commit {not_found_commit.id} not found{Fore.RESET}")


    def print_commit(self, definition: Definition, commit_definition: CommitDefinition, commit: Commit):
        if not isinstance(commit_definition, CommitDefinition):
            raise ValueError()
        if not isinstance(commit, Commit):
            raise ValueError()

        correct = commit_definition.is_correct
        limit_date = definition.limit_date

        short_hash = commit.short_hash()
        message = commit.short_message()
        commit_date = commit.committed_date

        color_title = Fore.GREEN if correct else Fore.RED
        print(f"==== {Style.BRIGHT}{Fore.BLUE}{short_hash}{Fore.RESET} - {color_title}{message}{Fore.RESET}{Style.RESET_ALL} ====", end=" ")
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
                print(Fore.RED + "COMPTE!! El tag ha segut modificat després de la data d'entrega" + Fore.RESET)

        print(commit_definition.checks)
        for check in commit_definition.checks:
            self.print_check(check)


    def print_check(self, check):
        self.checkFormatter[type(check).__name__](check)


    def print_branch_check(self, check):
        for branch, correct in check.branches.items():
            result = f"  {Fore.GREEN}YES{Fore.RESET}" if correct else f"{Fore.RED}NO{Fore.RESET}"
            print(f"  - Has {Fore.YELLOW}'{branch}'{Fore.RESET} branch? {result}")


    def print_diff_check(self, check):
        diff_correct = False #check.correct
        diff_result = f"{Fore.GREEN}YES{Fore.RESET}" if diff_correct else f"{Fore.RED}NO{Fore.RESET}"
        print(f"- Is diff correct? {diff_result}")
        if not diff_correct:
            print(f"    {Fore.YELLOW}Expected diff:{Fore.RESET}")
            for file, diff_index in check.diff.items():
                print(f"    {Fore.CYAN}- {file}{Fore.RESET}")
                if diff_index.additions:
                    for line, count in diff_index.additions.items():
                        print(f"      {count}+: {line}")
                if diff_index.deletions:
                    for line, count in diff_index.deletions.items():
                        print(f"      {count}-: {line}")

            print(f"    {Fore.YELLOW}Actual diff:{Fore.RESET}")
            for file, diff_index in commit.diff.items():
                print(f"    {Fore.CYAN}- {file}{Fore.RESET}")
                if diff_index.additions:
                    for line, count in diff_index.additions.items():
                        print(f"      {count}+: {line}")
                if diff_index.deletions:
                    for line, count in diff_index.deletions.items():
                        print(f"      {count}-: {line}")


    def print_tag_check(self, check):
        for tag, correct in check.tags.items():
            result = f"{Fore.GREEN}YES{Fore.RESET}" if correct else f"{Fore.RED}NO{Fore.RESET}"
            print(f"- Has {Fore.YELLOW}'{tag}'{Fore.RESET} tag? {result}")
