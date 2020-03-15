import logging

from stograde.common import chdir
from stograde.common import run


def pull(student: str, no_repo_update: bool):
    logging.debug("Pulling {}'s repository".format(student))
    with chdir(student):
        if not no_repo_update:
            run(['git', 'pull', '--quiet', 'origin', 'master'])
