from gitjudge.entity import DiffList, DiffIndex
from gitjudge.entity.checks import DiffCheck

def map_diff_check(d: dict) -> list:
    if not isinstance(d, dict):
        raise TypeError('Expected dict object')

    checks = []

    diff = d.get('diff', None)
    if diff:
        diff_list = DiffList()
        for file, text in diff.items():
            diffindex = DiffIndex(file)
            for line in text.split('\n'):
                if line.startswith('+'):
                    diffindex.add_addition(line[1:])
                elif line.startswith('-'):
                    diffindex.add_deletion(line[1:])
            diff_list.add(diffindex)

        checks.append(DiffCheck(diff_list))

    return checks
