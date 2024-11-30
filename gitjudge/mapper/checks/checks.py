from gitjudge.entity.checks import Check
from gitjudge.entity.diffindex import DiffIndex
from gitjudge.entity.difflist import DiffList

from .branch_check import map_branch_check
from .cherry_pick_check import map_cherry_pick_check
from .diff_check import map_diff_check
from .reverts_check import map_reverts_check
from .squash_check import map_squash_check
from .tag_check import map_tag_check


def map_checks(d: dict) -> []:
    if not isinstance(d, dict):
        raise TypeError('Expected dict object')

    checks = []

    checks = checks + map_branch_check(d)
    checks = checks + map_cherry_pick_check(d)
    checks = checks + map_diff_check(d)
    checks = checks + map_reverts_check(d)
    checks = checks + map_squash_check(d)
    checks = checks + map_tag_check(d)

    return checks
