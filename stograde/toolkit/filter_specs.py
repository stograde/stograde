from typing import List, Dict

from stograde.specs import check_dependencies, check_architecture
from stograde.specs.spec import Spec
from stograde.toolkit.stogradeignore import load_stogradeignore


def filter_assignments(assignments: List[str],
                       ci: bool) -> List[str]:
    filtered_assignments = set(assignments)

    if ci:
        ignored_assignments = load_stogradeignore()
        filtered_assignments = filtered_assignments.difference(ignored_assignments)

    return list(filtered_assignments)


def filter_specs(specs_to_record: List[str],
                 specs: Dict[str, Spec],
                 ci: bool) -> List[str]:
    remaining_specs = set(specs_to_record)
    for spec_id in specs_to_record:
        spec_to_use = specs[spec_id]
        try:
            check_dependencies(spec_to_use)
            if not check_architecture(spec_to_use, ci):
                remaining_specs.remove(spec_to_use.id)
        except KeyError:
            # Prevent lab0 directory from causing an extraneous output
            if spec_to_use.id != 'lab0':
                print('Spec {} does not exist'.format(spec_to_use.id), file=sys.stderr)
            remaining_specs.remove(spec_to_use.id)

    return list(remaining_specs)
