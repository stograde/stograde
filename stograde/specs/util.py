import os
import logging
import sys

from stograde.common import run


def get_filenames(spec):
    """returns the list of files from an assignment spec"""
    return [file['filename'] for file in spec['files'] if not file['options'].get('optional', False)]


def check_dependencies(spec):
    for filepath in spec.get('dependencies', []):
        try:
            os.stat(filepath)
        except FileNotFoundError:
            logging.warning('spec {}: required file "{}" could not be found'.format(spec['assignment'], filepath))


def check_architecture(assignment, spec, ci):
    # get check_architecture()
    _, arch, _ = run(['uname', '-m'])
    spec_arch = spec.get('architecture', None)
    if not spec_arch or spec_arch == arch:
        return True
    else:
        if ci:
            logging.info('Skipping {}: wrong architecture'.format(assignment))
        else:
            print('{} requires {} architecture. You have {}'
                  .format(assignment, spec['architecture'], arch),
                  file=sys.stderr)
        return False
