import logging

from cs251tk.common import chdir
from cs251tk.common import run


def pull(student, no_update):
    logging.debug("Pulling {}'s repository".format(student))
    with chdir(student):
        if not no_update:
            run(['git', 'pull', '--quiet', 'origin', 'master'])
