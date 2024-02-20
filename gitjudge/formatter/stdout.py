from colorama import Fore, Style

from gitjudge.entity import Commit, ExpectedCommit, CheckResult

def print_expected_commit(expected_commit: ExpectedCommit):
    def print_item(name, value):
        print(f"{name}: {Fore.YELLOW}{value}{Fore.RESET}")

    if expected_commit.start:
        print_item("Starting point", expected_commit.start)
    if expected_commit.message:
        print_item("Message", expected_commit.message)
    if expected_commit.tags:
        print_item("Tags", expected_commit.tags)
    if expected_commit.branches:
        print_item("Branches", expected_commit.branches)
    if expected_commit.parents:
        print_item("Parents", expected_commit.parents)

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

    if check_result.has_checked_cherry_pick():
        if not check_result.has_found_cherry_pick_commit():
            print(f"- Cherry-picked from commit {Fore.RED}not found{Fore.RESET}.")
        else:
            cherry_picked = check_result.is_cherry_picked()
            cherry_pick_result = f"{Fore.GREEN}YES{Fore.RESET}" if cherry_picked else f"{Fore.RED}NO{Fore.RESET}"
            cherry_pick_id = check_result.cherry_picked_from_commit.id
            cherry_pick_short_hash = check_result.cherry_picked_from_commit.short_hash()
            print(f"- Is cherry-picked from {Fore.YELLOW}'({cherry_pick_id}) {cherry_pick_short_hash}'{Fore.RESET}? {cherry_pick_result}")


    if check_result.has_checked_revert():
        if not check_result.has_found_reverted_commit():
            print(f"- Reverting commit {Fore.RED}not found{Fore.RESET}.")
        else:
            reverts = check_result.is_reverted()
            revert_result = f"{Fore.GREEN}YES{Fore.RESET}" if reverts else f"{Fore.RED}NO{Fore.RESET}"
            revert_id = check_result.reverted_from_commit.id
            revert_short_hash = check_result.reverted_from_commit.short_hash()
            print(f"- Reverts {Fore.YELLOW}'({revert_id}) {revert_short_hash}'{Fore.RESET}? {revert_result}")

    for tag, valid in check_result.tags.items():
        tag_result = f"{Fore.GREEN}YES{Fore.RESET}" if valid else f"{Fore.RED}NO{Fore.RESET}"
        print(f"- Has {Fore.YELLOW}'{tag}'{Fore.RESET} tag? {tag_result}")
