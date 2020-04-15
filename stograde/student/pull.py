import logging
import sys

from ..common import chdir, run
from ..common.run_status import RunStatus


def pull(student: str):
    logging.debug("Pulling {}'s repository".format(student))
    with chdir(student):
        status, output, _ = run(['git', 'pull', '--quiet', 'origin', 'master'])

    if status is RunStatus.CALLED_PROCESS_ERROR and 'not a git repository' in output:
        print('Student directory {} is not a git repository'.format(student), file=sys.stderr)
        print('Try running "stograde repo reclone"', file=sys.stderr)
