from .warning_unmerged_branches import find_unmerged_branches


def find_warnings():
    return {'unmerged branches': find_unmerged_branches()}
