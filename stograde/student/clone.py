import logging
import sys
from os import path

from ..common import run
from ..common.run_status import RunStatus


def clone_student(student: str, base_url: str):
    logging.debug("Cloning {}'s repository".format(student))
    if not path.exists(student):
        clone_url('{}/{}.git'.format(base_url, student))


def clone_url(url: str, into: str = None):
    if into:
        logging.info('cloning {} into {}'.format(url, into))
        status, output, _ = run(['git', 'clone', '--quiet', url, into])
    else:
        logging.info('cloning {}'.format(url))
        status, output, _ = run(['git', 'clone', '--quiet', url])
    logging.debug(output)
    if status is RunStatus.CALLED_PROCESS_ERROR and 'Permission denied' in output:
        print('Permission denied when cloning from {}.\n'
              'Make sure that this SSH key is registered with StoGit.'.format(url),
              file=sys.stderr)
        sys.exit(1)
