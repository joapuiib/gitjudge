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
    for category, items in checks.items():
        for k, valid in items.items():
            if not valid:
                correct = False
                break

    short_hash = commit.short_hash()
    message = commit.message
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

    if checks.get("tags", None):
        for tag, valid in checks["tags"].items():
            tag_result = f"{Fore.GREEN}YES{Fore.RESET}" if valid else f"{Fore.RED}NO{Fore.RESET}"
            print(f"- Has {Fore.YELLOW}'{tag}'{Fore.RESET} tag? {tag_result}")
