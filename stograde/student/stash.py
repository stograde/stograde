import logging

from ..common import chdir, run


def stash(student: str, no_repo_update: bool = False):
    logging.debug("Stashing {}'s repository".format(student))
    with chdir(student):
        if not no_repo_update and has_changed_files():
            run(['git', 'stash', '-u'])
            run(['git', 'stash', 'clear'])


def has_changed_files() -> bool:
    _, output, _ = run(['git', 'status', '--porcelain'])
    return bool(output)
