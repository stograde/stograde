import datetime
import logging
import os.path
import sys
from os import getcwd
from typing import Dict, TYPE_CHECKING

from .args import process_args
from stograde.specs.download_specs import create_data_dir
from stograde.specs.filter_specs import filter_assignments, find_all_specs
from .find_update import update_available
from .stogit_url import compute_stogit_url
from ..specs import load_specs

if TYPE_CHECKING:
    from ..specs.spec import Spec


def main():
    base_dir = getcwd()
    args, students, assignments = process_args()
    course: str = args['course']
    command_func = args['func']
    skip_version_check: bool = args['skip_version_check']
    stogit: str = args['stogit']

    if not skip_version_check:
        current_version, new_version = update_available()
        if new_version:
            print(('v{} is available: you have v{}. '
                   'Try "pip3 install --no-cache --user --upgrade stograde" '
                   'to update.').format(new_version, current_version), file=sys.stderr)

    if not os.path.exists("data"):
        create_data_dir(course, base_dir)

    stogit_url = compute_stogit_url(stogit=stogit, course=course, _now=datetime.date.today())

    if args['command'] == 'repo':
        command_func(students=students,
                     stogit_url=stogit_url,
                     no_progress_bar=args['no_progress_bar'],
                     workers=args['workers'])
        sys.exit(0)
    elif args['command'] == 'table':
        assignments = [path.split('/')[-1].split('.')[0]
                       for path in find_all_specs(os.path.join(base_dir, 'data', 'specs'))]

    date: str = args['date']
    skip_spec_update: bool = args['skip_spec_update']

    if date:
        logging.debug('Checking out {}'.format(date))

    assignments = filter_assignments(assignments)

    loaded_specs: Dict[str, 'Spec'] = load_specs(assignments,
                                                 data_dir=os.path.join(base_dir, 'data'),
                                                 skip_spec_update=skip_spec_update)

    if not loaded_specs:
        print('No specs loaded!')
        sys.exit(1)

    # Call function to handle subcommand
    command_func(specs=loaded_specs,
                 students=students,
                 base_dir=base_dir,
                 stogit_url=stogit_url,
                 args=args)
