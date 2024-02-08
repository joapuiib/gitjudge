#!/usr/bin/env python3

import git
import subprocess
import subprocess
from datetime import datetime
from colorama import Fore, Style

from pygments import highlight as highlight_py
from pygments.lexers import get_lexer_by_name
from pygments.formatters import Terminal256Formatter
def highlight(text, syntax, light=False):
    theme = "monokai"
    if light:
        theme = "solarized-light"

    return highlight_py(text, get_lexer_by_name(syntax), Terminal256Formatter(style=theme))

def print_java_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"Content of '{file_path}':\n")
            print(highlight(content, "java"))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

repo = git.Repo(".")

def get_short_commit_hash(commit):
    return commit.repo.git.rev_parse(commit.hexsha, short=True)

def find_latest_commit_by_message(target_message):
    for commit in repo.iter_commits():
        if target_message.lower() in commit.message.lower():
            return commit

    return None

def does_branch_exist(branch_name):
    return True
    try:
        repo.git.rev_parse('--verify', f'refs/heads/{branch_name}')
        return True
    except git.GitCommandError:
        return False


def find_commit_by_message(parent_commit, target_message, branch=None):
    if parent_commit is None:
        return None

    if branch is None or branch == "DEFAULT":
        default_branch_ref = repo.git.symbolic_ref('HEAD', quiet=True)
        branch = default_branch_ref.split('/')[-1]

    if not does_branch_exist(branch):
        return None;

    for commit in repo.iter_commits(rev=f'{parent_commit}..{branch}'):
        if target_message.lower() in commit.message.lower():
            return commit;

def find_merge_commit(parent1, parent2):
    # Iterate through commits
    for commit in repo.iter_commits():
        parent_hashes = [parent.hexsha for parent in commit.parents]

        # Check if the commit is a merge commit with the specified parents
        if len(commit.parents) == 2 and parent1.hexsha in parent_hashes and parent2.hexsha in parent_hashes:
            return commit

    return None

def show_commit(commit):
    show_output = repo.git.show(commit.hexsha, color='always')
    # Find the start of the diff section
    diff_start = show_output.find('@@')

    # Print only the diff section
    if diff_start != -1:
        print(show_output[diff_start:])

    print()

def contains_diff(commit, diff):
    show_output = repo.git.show(commit.hexsha)
    return show_output.find(diff.strip()) != -1

def is_commit_in_branch(commit, branch_name):
    return repo.git.branch('--contains', commit.hexsha).find(branch_name) != -1

def is_branch_at_commit(commit, branch_name):
    if not does_branch_exist(branch_name):
        return False;

    # Get the commit hash of the branch's HEAD
    branch_head_commit_hash = repo.git.rev_parse(f'{branch_name}^{{commit}}')

    # Check if the branch is at the expected commit
    return branch_head_commit_hash == commit.hexsha

def check_commit(commit, diff, in_branches=[], at_branches=[], limit_date=None):
    if commit is None:
        print(f"{Fore.RED}Commit not found!{Fore.RESET}")
        return

    correct = contains_diff(commit, diff)
    short_hash = get_short_commit_hash(commit)
    message = commit.message.replace("\n", "")

    color_title = Fore.GREEN if correct else Fore.RED
    print(f"==== {Style.BRIGHT}{Fore.BLUE}{short_hash}{Fore.RESET} - {color_title}{message}{Fore.RESET}{Style.RESET_ALL} ====", end=" ")

    if correct:
        print(f"{Fore.GREEN}OK!{Fore.RESET}")
    else:
        print(f"{Fore.RED}ERROR!{Fore.RESET}")
        show_commit(commit)

    if limit_date:
        limit_date = datetime.fromisoformat(limit_date)
        seconds_since_epoch = commit.committed_date
        commit_date = datetime.fromtimestamp(seconds_since_epoch)
        print(f"Limit date: {limit_date}")
        print(f"Last change: {commit_date}")
        if commit_date > limit_date:
            print(Fore.RED + "COMPTE!! El tag ha segut modificat després de la data d'entrega" + Fore.RESET)


    for b in in_branches:
        if b == "DEFAULT":
            b = default_branch_ref = repo.git.symbolic_ref('HEAD', quiet=True).split('/')[-1]
        is_in = is_commit_in_branch(commit, b)
        is_in_result = f"{Fore.GREEN}YES{Fore.RESET}" if is_in else f"{Fore.RED}NO{Fore.RESET}"
        print(f"- Belongs to {Fore.YELLOW}'{b}'{Fore.RESET} branch? {is_in_result}")

    for b in at_branches:
        if b == "DEFAULT":
            b = default_branch_ref = repo.git.symbolic_ref('HEAD', quiet=True).split('/')[-1]
        is_at = is_branch_at_commit(commit, b)
        is_at_result = f"{Fore.GREEN}YES{Fore.RESET}" if is_at else f"{Fore.RED}NO{Fore.RESET}"
        print(f"- Is branch {Fore.YELLOW}'{b}'{Fore.RESET} at this commit? {is_at_result}")

    print()

def show_log(commit_start, commit_end):
    git_log_command = "git log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all"

    short_start = "" if commit_start is None else get_short_commit_hash(commit_start)
    short_end = "" if commit_end is None else get_short_commit_hash(commit_end)
    if commit_start is not None or commit_end is not None:
        git_log_command = git_log_command + f" {short_start}^..{short_end}"

    try:
        print("Git Log between commits:")
        result = subprocess.run(git_log_command, shell="True")
    except subprocess.CalledProcessError as e:
        # Print the error if the command fails
        print("Error:", e)
        print("Command Output:")
        print(e.stdout)
        print("Command Error Output:")
        print(e.stderr)

limit_date = "2023-11-05 23:59:00"

# multiplytablefull = find_latest_commit_by_message("Fixed first operator")
multiplytablefull = find_latest_commit_by_message("Added MultiplyTableFull")
multiplytablefull_diff = """
+package ud2.practices;
+
+import java.util.Scanner;
+import java.util.Locale;
+
+public class MultiplyTableFull {
+    public static void main(String[] args) {
+        Scanner in = new Scanner(System.in).useLocale(Locale.US);
+
+        for (int i = 1; i <= 10; i++) {
+            for (int j = 5; j <= 20; j++) {
+                System.out.printf(" %3d", i*j);
+            }
+            System.out.println();
+        }
+    }
+}
"""
check_commit(multiplytablefull, multiplytablefull_diff, in_branches=["DEFAULT"], limit_date=limit_date)

ask_n_user = find_commit_by_message(multiplytablefull, "Added functionality: Ask N to the user")
ask_n_user_diff = """
 public class MultiplyTableFull {
     public static void main(String[] args) {
         Scanner in = new Scanner(System.in).useLocale(Locale.US);
+        int n = in.nextInt();
 
         for (int i = 1; i <= 10; i++) {
             for (int j = 5; j <= 20; j++) {
"""
check_commit(ask_n_user, ask_n_user_diff, in_branches=["DEFAULT"], at_branches=["origin/p2/ask_n_user"], limit_date=limit_date)


fix_repetitions = find_commit_by_message(multiplytablefull, "Fixed repetitions")
fix_repetitions_diff = """
         Scanner in = new Scanner(System.in).useLocale(Locale.US);
 
         for (int i = 1; i <= 10; i++) {
-            for (int j = 5; j <= 20; j++) {
+            for (int j = 5; j <= n; j++) {
                 System.out.printf(" %3d", i*j);
             }
             System.out.println();
"""
check_commit(fix_repetitions, fix_repetitions_diff, in_branches=["DEFAULT"], at_branches=["origin/p2/fix_repetitions"], limit_date=limit_date)

origin_fix_first_operator = find_commit_by_message(multiplytablefull, "Fixed first operator", "origin/p2/fix_first_operator")
origin_fix_first_operator_diff = """
         Scanner in = new Scanner(System.in).useLocale(Locale.US);
 
         for (int i = 1; i <= 10; i++) {
-            for (int j = 5; j <= 20; j++) {
+            for (int j = 1; j <= 20; j++) {
                 System.out.printf(" %3d", i*j);
             }
             System.out.println();
"""
check_commit(origin_fix_first_operator, origin_fix_first_operator_diff, at_branches=["origin/p2/fix_first_operator"], limit_date=limit_date)

merge = find_merge_commit(ask_n_user, fix_repetitions)
merge_diff = """
  public class MultiplyTableFull {
      public static void main(String[] args) {
          Scanner in = new Scanner(System.in).useLocale(Locale.US);
 +        int n = in.nextInt();
  
          for (int i = 1; i <= 10; i++) {
-             for (int j = 5; j <= 20; j++) {
+             for (int j = 5; j <= n; j++) {
                  System.out.printf(" %3d", i*j);
              }
              System.out.println();
"""
check_commit(merge, merge_diff, in_branches=["DEFAULT"], limit_date=limit_date)

rebased_fix_first_operator = find_commit_by_message(merge, "Fixed first operator")
rebased_fix_first_operator_diff = """
         int n = in.nextInt();
 
         for (int i = 1; i <= 10; i++) {
-            for (int j = 5; j <= n; j++) {
+            for (int j = 1; j <= n; j++) {
                 System.out.printf(" %3d", i*j);
             }
             System.out.println();
"""
check_commit(rebased_fix_first_operator, rebased_fix_first_operator_diff, in_branches=["DEFAULT"], limit_date=limit_date)

show_log(multiplytablefull, rebased_fix_first_operator)
print()

print_java_file("src/main/java/ud2/practices/MultiplyTableFull.java")
