import logging

from stograde.common import chdir
from stograde.common import run


def stash(student, no_update):
    logging.debug("Stashing {}'s repository".format(student))
    with chdir(student):
        if not no_update and has_changed_files():
            run(['git', 'stash', '-u'])
            run(['git', 'stash', 'clear'])


def has_changed_files():
    _, output, _ = run(['git', 'status', '--porcelain'])
    return bool(output)
