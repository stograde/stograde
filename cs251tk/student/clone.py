import logging
from os import path
from cs251tk.common import run


def clone_student(student, baseurl):
    if not path.exists(student):
        clone_url('{}/{}.git'.format(baseurl, student))


def clone_url(url, into=None):
    if into:
        logging.info('cloning {} into {}'.format(url, into))
        _, output, _ = run(['git', 'clone', '--quiet', url, into])
    else:
        logging.info('cloning {}'.format(url))
        _, output, _ = run(['git', 'clone', '--quiet', url])
    logging.debug(output)
