from colorama import Fore, Style

from gitjudge.entity import Commit, CommitDefinition, CheckResult, NotFoundCommit, ReferencedItselfCommit

def print_commit_definition(commit_definition: CommitDefinition):
    def print_item(name, value):
        print(f"{name}: {Fore.YELLOW}{value}{Fore.RESET}")

    if commit_definition.start:
        if isinstance(commit_definition.start, NotFoundCommit):
            print_item(f"Start", f"({commit_definition.start.id}) {Fore.RED}not found{Fore.RESET}")
        elif isinstance(commit_definition.start, Commit):
            print_item(f"Start", f"({commit_definition.start.id}) {commit_definition.start.short_hash()}")

    if commit_definition.end:
        if isinstance(commit_definition.end, NotFoundCommit):
            print_item(f"End", f"({commit_definition.end.id}) {Fore.RED}not found{Fore.RESET}")
        elif isinstance(commit_definition.end, Commit):
            print_item(f"End", f"({commit_definition.end.id}) {commit_definition.end.short_hash()}")

    if commit_definition.message:
        print_item("Message", commit_definition.message)
    if commit_definition.tags:
        print_item("Tags", commit_definition.tags)
    if commit_definition.branches:
        print_item("Branches", commit_definition.branches)
    if commit_definition.parents:
        print_item("Parents", commit_definition.parents)


def print_not_found_commit(not_found_commit: NotFoundCommit):
    print(f"{Fore.RED}Commit {not_found_commit.id} not found{Fore.RESET}")


def print_commit(commit: Commit, check_result: CheckResult, limit_date: str = None):
    correct = check_result.is_correct()

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

    for branch, valid in check_result.branches.items():
        branch_result = f"{Fore.GREEN}YES{Fore.RESET}" if valid else f"{Fore.RED}NO{Fore.RESET}"
        print(f"- Is in {Fore.YELLOW}'{branch}'{Fore.RESET} branch? {branch_result}")

    for tag, valid in check_result.tags.items():
        tag_result = f"{Fore.GREEN}YES{Fore.RESET}" if valid else f"{Fore.RED}NO{Fore.RESET}"
        print(f"- Has {Fore.YELLOW}'{tag}'{Fore.RESET} tag? {tag_result}")

    if check_result.cherry_pick:
        if isinstance(check_result.cherry_pick, NotFoundCommit):
            print(f"- Cherry-picked from commit ({check_result.cherry_pick.id}) {Fore.RED}not found{Fore.RESET}.")
        elif isinstance(check_result.cherry_pick, ReferencedItselfCommit):
            print(f"- Cherry-picked from commit {Fore.RED}can't reference itself{Fore.RESET}.")
        else:
            cherry_picked = check_result.is_cherry_picked
            cherry_pick_result = f"{Fore.GREEN}YES{Fore.RESET}" if cherry_picked else f"{Fore.RED}NO{Fore.RESET}"
            cherry_pick_id = check_result.cherry_pick.id
            cherry_pick_short_hash = check_result.cherry_pick.short_hash()
            print(f"- Is cherry-picked from {Fore.YELLOW}'({cherry_pick_id}) {cherry_pick_short_hash}'{Fore.RESET}? {cherry_pick_result}")


    if check_result.reverts:
        if isinstance(check_result.reverts, NotFoundCommit):
            print(f"- Reverting commit ({check_result.reverts.id}) {Fore.RED}not found{Fore.RESET}.")
        elif isinstance(check_result.reverts, ReferencedItselfCommit):
            print(f"- Reverting commit {Fore.RED}can't reference itself{Fore.RESET}.")
        else:
            reverts = check_result.is_reverted
            revert_result = f"{Fore.GREEN}YES{Fore.RESET}" if reverts else f"{Fore.RED}NO{Fore.RESET}"
            revert_id = check_result.reverts.id
            revert_short_hash = check_result.reverts.short_hash()
            print(f"- Reverts {Fore.YELLOW}'({revert_id}) {revert_short_hash}'{Fore.RESET}? {revert_result}")

    if check_result.squashes:
        squashes = check_result.is_squashed
        squash_result = f"{Fore.GREEN}YES{Fore.RESET}" if squashes else f"{Fore.RED}NO{Fore.RESET}"
        squash_output = ", ".join([f"{commit.short_hash()}" for commit in check_result.squashes])
        print(f"- Does squash {Fore.YELLOW}'{squash_output}'{Fore.RESET}? {squash_result}")

    if check_result.diff:
        diff_correct = check_result.is_diff
        diff_result = f"{Fore.GREEN}YES{Fore.RESET}" if diff_correct else f"{Fore.RED}NO{Fore.RESET}"
        print(f"- Is diff correct? {diff_result}")
        if not diff_correct:
            print(f"    {Fore.YELLOW}Expected diff:{Fore.RESET}")
            for file, diff_index in check_result.diff.items():
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

    if check_result.file_content:
        file_content_correct = check_result.is_file_content
        file_content_result = f"{Fore.GREEN}YES{Fore.RESET}" if file_content_correct else f"{Fore.RED}NO{Fore.RESET}"
        if not file_content_correct:
            for file, content in check_result.file_content.items():
                print(f"- {Fore.CYAN}{file}{Fore.RESET}:")
                print(f"    {Fore.YELLOW}Expected:{Fore.RESET}")
                print(f"    {check_result.file_content[file]}")
                print(f"    {Fore.YELLOW}Actual:{Fore.RESET}")
                print(f"    {commit.get_file_content(file)}")
