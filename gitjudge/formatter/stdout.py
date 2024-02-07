from colorama import Fore, Style

from gitjudge.entity import Commit, ExpectedCommit

def print_expected_commit(expected_commit: ExpectedCommit):
    def print_item(name, value):
        print(f"{name}: {Fore.YELLOW}{value}{Fore.RESET}")

    if expected_commit.starting_point:
        print_item("Starting point", expected_commit.starting_point)
    if expected_commit.message:
        print_item("Message", expected_commit.message)
    if expected_commit.tags:
        print_item("Tags", expected_commit.tags)
    if expected_commit.branches:
        print_item("Branches", expected_commit.branches)
    if expected_commit.parents:
        print_item("Parents", expected_commit.parents)

def print_commit(commit: Commit, checks: dict, limit_date: str = None):
    correct = True
    for category, item in checks.items():
        if isinstance(item, dict):
            for k, valid in item.items():
                if not valid:
                    correct = False
                    break
        elif isinstance(item, bool):
            if not item:
                correct = False
                break

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

    if checks.get("cherry_pick") != None:
        if not commit.cherry_picked_from:
            print(f"- Cherry-picked from commit {Fore.RED}not found{Fore.RESET}.")
        else:
            cherry_picked = commit.is_cherry_picked
            cherry_pick_result = f"{Fore.GREEN}YES{Fore.RESET}" if cherry_picked else f"{Fore.RED}NO{Fore.RESET}"
            cherry_pick_id = commit.cherry_picked_from.id
            cherry_pick_short_hash = commit.cherry_picked_from.short_hash()
            print(f"- Is cherry-picked from {Fore.YELLOW}'({cherry_pick_id}) {cherry_pick_short_hash}'{Fore.RESET}? {cherry_pick_result}")

    if checks.get("reverts") != None:
        if not commit.reverting_commit:
            print(f"- Reverting commit {Fore.RED}not found{Fore.RESET}.")
        else:
            reverts = commit.reverts
            revert_result = f"{Fore.GREEN}YES{Fore.RESET}" if reverts else f"{Fore.RED}NO{Fore.RESET}"
            revert_id = commit.reverting_commit.id
            revert_short_hash = commit.reverting_commit.short_hash()
            print(f"- Reverts {Fore.YELLOW}'({revert_id}) {revert_short_hash}'{Fore.RESET}? {revert_result}")

    if checks.get("tags", None):
        for tag, valid in checks["tags"].items():
            tag_result = f"{Fore.GREEN}YES{Fore.RESET}" if valid else f"{Fore.RED}NO{Fore.RESET}"
            print(f"- Has {Fore.YELLOW}'{tag}'{Fore.RESET} tag? {tag_result}")
