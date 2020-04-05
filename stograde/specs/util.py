import os
import logging
import sys
from typing import List, TYPE_CHECKING

from ..common.run import run
from ..toolkit.global_vars import CI

if TYPE_CHECKING:
    from ..specs.spec import Spec


def get_filenames(spec: 'Spec') -> List[str]:
    """returns the list of files from an assignment spec"""
    return [file.file_name for file in spec.files if not file.options.optional]


def check_dependencies(spec: 'Spec'):
    for filepath in spec.dependencies:
        try:
            os.stat(filepath)
        except FileNotFoundError:
            logging.warning('spec {}: required file "{}" could not be found'.format(spec.id, filepath))


def check_architecture(spec: 'Spec') -> bool:
    _, user_arch, _ = run(['uname', '-m'])
    user_arch = user_arch.rstrip()
    spec_arch = spec.architecture

    if spec_arch is None or spec_arch == user_arch:
        return True
    else:
        if CI:
            logging.info('Skipping {}: wrong architecture'.format(spec.id))
        else:
            print('{} requires {} architecture. You have {}'
                  .format(spec.id, spec.architecture, user_arch),
                  file=sys.stderr)
        return False
