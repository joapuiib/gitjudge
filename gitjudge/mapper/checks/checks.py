from .branch_check import map_branch_check
from .cherry_pick_check import map_cherry_pick_check
from .diff_check import map_diff_check
from .file_content_check import map_file_content_check
from .reverts_check import map_reverts_check
from .squash_check import map_squash_check
from .tag_check import map_tag_check


def map_checks(d: dict) -> list:
    if not isinstance(d, dict):
        raise TypeError("Expected dict object")

    checks = []

    checks = checks + map_branch_check(d)
    checks = checks + map_cherry_pick_check(d)
    checks = checks + map_diff_check(d)
    checks = checks + map_file_content_check(d)
    checks = checks + map_reverts_check(d)
    checks = checks + map_squash_check(d)
    checks = checks + map_tag_check(d)

    return checks
