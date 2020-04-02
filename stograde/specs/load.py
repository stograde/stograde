from glob import iglob
import logging
import os
import sys
from typing import List, Dict

from .spec import create_spec, Spec
from ..common import chdir
from ..common.run import run


def load_all_specs(data_dir: str, skip_update_check: bool = True) -> Dict[str, Spec]:
    return load_specs(find_all_specs(spec_dir=os.path.join(data_dir, 'specs')),
                      data_dir=data_dir,
                      skip_update_check=skip_update_check)


def load_specs(wanted_spec_files: List[str], data_dir: str, skip_update_check: bool = True) -> Dict[str, Spec]:
    os.makedirs(data_dir, exist_ok=True)

    if not skip_update_check:
        check_for_spec_updates(data_dir)

    # the repo has a /specs folder
    spec_dir = os.path.join(data_dir, 'specs')

    all_spec_files = find_all_specs(spec_dir)
    loadable_spec_files = set(all_spec_files).intersection(wanted_spec_files)
    missing_spec_files = set(wanted_spec_files).difference(all_spec_files)

    for spec in missing_spec_files:
        logging.warning("No spec for {}".format(spec))

    loaded_specs = [create_spec(filename, spec_dir) for filename in loadable_spec_files]

    return {spec.id: spec for spec in loaded_specs}


def find_all_specs(spec_dir: str) -> List[str]:
    return iglob(os.path.join(spec_dir, '*.yaml'))


def check_for_spec_updates(data_dir: str):
    with chdir(data_dir):
        res, _, _ = run(['git', 'fetch', 'origin'])

        if res != 'success':
            print("Error fetching specs", file=sys.stderr)

        _, res, _ = run(['git', 'log', 'HEAD..origin/master'])

    if res != '':
        print("Spec updates found - Updating", file=sys.stderr)
        with chdir(data_dir):
            run(['git', 'pull', 'origin', 'master'])
