from colorama import Fore, Style

from gitjudge.entity import Commit, ExpectedCommit, CheckResult, NotFoundCommit, ReferencedItselfCommit

def print_expected_commit(expected_commit: ExpectedCommit):
    def print_item(name, value):
        print(f"{name}: {Fore.YELLOW}{value}{Fore.RESET}")

    if expected_commit.start:
        if isinstance(expected_commit.start, NotFoundCommit):
            print_item(f"Start", f"({expected_commit.start.id}) {Fore.RED}not found{Fore.RESET}")
        elif isinstance(expected_commit.start, Commit):
            print_item(f"Start", f"({expected_commit.start.id}) {expected_commit.start.short_hash()}")

    if expected_commit.end:
        if isinstance(expected_commit.end, NotFoundCommit):
            print_item(f"End", f"({expected_commit.end.id}) {Fore.RED}not found{Fore.RESET}")
        elif isinstance(expected_commit.end, Commit):
            print_item(f"End", f"({expected_commit.end.id}) {expected_commit.end.short_hash()}")

    if expected_commit.message:
        print_item("Message", expected_commit.message)
    if expected_commit.tags:
        print_item("Tags", expected_commit.tags)
    if expected_commit.branches:
        print_item("Branches", expected_commit.branches)
    if expected_commit.parents:
        print_item("Parents", expected_commit.parents)


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

    for tag, valid in check_result.tags.items():
        tag_result = f"{Fore.GREEN}YES{Fore.RESET}" if valid else f"{Fore.RED}NO{Fore.RESET}"
        print(f"- Has {Fore.YELLOW}'{tag}'{Fore.RESET} tag? {tag_result}")
