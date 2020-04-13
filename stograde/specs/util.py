import os
import logging
import sys
from typing import List, TYPE_CHECKING

from ..common.run import run
from ..toolkit import global_vars

if TYPE_CHECKING:
    from ..specs.spec import Spec


def get_filenames(spec: 'Spec') -> List[str]:
    """Returns the list of names of required files from an assignment spec"""
    return [file.file_name for file in spec.files if not file.options.optional]


def check_spec_dependencies(spec: 'Spec'):
    all_dependencies_present = True
    for filepath in spec.dependencies:
        try:
            os.stat(filepath)
        except FileNotFoundError:
            logging.warning('spec {}: required file "{}" could not be found'.format(spec.id, filepath))
            all_dependencies_present = False
    return all_dependencies_present


def check_architecture(spec: 'Spec') -> bool:
    """Checks that the user is running the right architecture to test this spec"""
    _, user_arch, _ = run(['uname', '-m'])
    user_arch = user_arch.rstrip()
    spec_arch = spec.architecture

    if spec_arch is None or spec_arch == user_arch:
        return True
    else:
        if global_vars.CI:
            logging.info('Skipping {}: wrong architecture'.format(spec.id))
        else:
            print('{} requires {} architecture. You have {}'
                  .format(spec.id, spec.architecture, user_arch),
                  file=sys.stderr)
        return False
