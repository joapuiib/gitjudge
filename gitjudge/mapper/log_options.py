from gitjudge.entity import LogOptions

def map_log_options(d: dict):
    log_options = LogOptions()

    if not isinstance(d, dict):
        raise TypeError("map_log_options: Expected a dict")

    if d.get("branches"):
        log_options.branches = d["branches"]

    if d.get("all"):
        log_options.all = d["all"]

    return log_options
