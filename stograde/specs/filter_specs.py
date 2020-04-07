import logging
import os
import sys
from glob import iglob
from typing import Dict, List, TYPE_CHECKING

from .stogradeignore import load_stogradeignore
from ..specs.util import check_architecture, check_dependencies
from ..toolkit import global_vars

if TYPE_CHECKING:
    from stograde.specs.spec import Spec


def filter_assignments(assignments: List[str]) -> List[str]:
    """Removes any assignments ignored by a .stogradeignore file"""
    filtered_assignments = set(assignments)

    if global_vars.CI:
        ignored_assignments = load_stogradeignore()
        filtered_assignments = filtered_assignments.difference(ignored_assignments)

    return list(filtered_assignments)


def get_spec_paths(wanted_specs: List[str], spec_dir: str) -> List[str]:
    """Removes any missing specs from the list and returns a list of the paths
    of the remaining specs"""
    all_spec_files = find_all_specs(spec_dir)
    loadable_spec_files = {path.split('/')[-1].split('.')[0]: path for path in list(all_spec_files)}
    specs_to_load = set(loadable_spec_files.keys()).intersection(wanted_specs)
    missing_spec_files = set(wanted_specs).difference(loadable_spec_files.keys())

    for spec in missing_spec_files:
        logging.warning("No spec for {}".format(spec))

    return list(loadable_spec_files[filename] for filename in specs_to_load)


def find_all_specs(spec_dir: str):
    """Get a list of all .yaml files in the specs directory"""
    return list(iglob(os.path.join(spec_dir, '*.yaml')))


def filter_loaded_specs(specs: Dict[str, 'Spec']) -> Dict[str, 'Spec']:
    """Filters the loaded specs based on properties such as required architecture"""
    remaining_specs: Dict[str, 'Spec'] = {}

    for spec_id in specs.keys():
        spec_to_use = specs[spec_id]
        try:
            check_dependencies(spec_to_use)
            if not check_architecture(spec_to_use):
                continue
        except KeyError:
            # Prevent lab0 directory from causing an extraneous output
            if spec_to_use.id != 'lab0':
                print('Spec {} does not exist'.format(spec_to_use.id), file=sys.stderr)
            continue
        remaining_specs[spec_id] = spec_to_use

    return remaining_specs
