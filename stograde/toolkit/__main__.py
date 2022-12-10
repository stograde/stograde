import datetime
import logging
import os.path
import sys
from os import getcwd
from typing import TYPE_CHECKING, List

from . import global_vars
from .args import process_args
from .check_dependencies import check_dependencies
from .create_students_dir import create_students_dir
from .find_update import update_available
from .stogit_url import compute_stogit_url
from ..specs import create_data_dir, filter_assignments, find_all_specs, load_specs

if TYPE_CHECKING:
    from ..specs.spec import Spec


def main():
    base_dir = getcwd()
    args, students, assignments = process_args()  # Dict[str, Any], List[str], List[str]
    branch: str = args.get('branch', 'main')
    command: str = args['command']  # The name of the SubCommand specified
    command_func = args['func']  # The function associated with the SubCommand
    course: str = args.get('course', '')
    skip_dependency_check: bool = args['skip_dependency_check']
    skip_version_check: bool = args['skip_version_check']
    stogit: str = args.get('stogit', '')

    if not skip_version_check:
        current_version, new_version = update_available()
        if new_version:
            print(('v{} is available: you have v{}. '
                   'Try "pip3 install --no-cache --user --upgrade stograde" '
                   'to update.').format(new_version, current_version), file=sys.stderr)

    if command == 'drive':
        # command_func will be do_drive()
        command_func(students=students,
                     assignment=assignments[0],
                     args=args)
        return  # stograde drive does not use the functionality below, so return

    if not skip_dependency_check:
        check_dependencies()

    if not os.path.exists('data'):
        create_data_dir(course, base_dir)

    stogit_url = compute_stogit_url(stogit=stogit, course=course, _now=datetime.date.today())

    if not os.path.exists('students') and command != 'ci':
        create_students_dir(base_dir=base_dir)

    if command == 'repo':
        # command_func will be do_repo_clean() or do_repo_update()
        command_func(students=students,
                     stogit_url=stogit_url,
                     branch=branch,
                     base_dir=base_dir,
                     no_progress_bar=args['no_progress_bar'],
                     workers=args['workers'])
        return  # stograde repo does not use the functionality below, so return

    if command == 'table':
        assignments = [path.split('/')[-1].split('.')[0]
                       for path in find_all_specs(os.path.join(base_dir, 'data', 'specs'))]

    date: str = args.get('date', '')
    skip_spec_update: bool = args.get('skip_spec_update', False)

    if date:
        print('Checking out {}'.format(date))

    assignments = filter_assignments(assignments)

    loaded_specs: List['Spec'] = load_specs(assignments,
                                            data_dir=os.path.join(base_dir, 'data'),
                                            skip_spec_update=skip_spec_update)

    if not loaded_specs:
        if global_vars.CI:
            logging.warning('No assignments detected!')
            sys.exit(0)
        else:
            print('No specs loaded!', file=sys.stderr)
            sys.exit(1)

    # Call function associated with specified SubCommand
    # command_func will be do_ci(), do_record(), do_table() or do_web()
    command_func(specs=loaded_specs,
                 students=students,
                 base_dir=base_dir,
                 stogit_url=stogit_url,
                 branch=branch,
                 args=args)
