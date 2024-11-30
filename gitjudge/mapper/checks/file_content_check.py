from gitjudge.entity.checks import FileContentCheck


def map_file_content_check(d: dict) -> list:
    if not isinstance(d, dict):
        raise TypeError('Expected dict object')

    checks = []

    file_contents = d.get('file_content', None)
    if file_contents:
        checks.append(FileContentCheck(file_contents))

    return checks
