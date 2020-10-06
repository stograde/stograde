"""Deal with argument parsing for the toolkit"""

import argparse
import logging
import os
import re
import sys
from glob import glob
from typing import Any, Dict, List, Tuple

from natsort import natsorted

from . import global_vars
from .get_students import get_students
from .subcommands import do_ci, do_drive, do_record, do_repo_clean, do_repo_update, do_table, do_web
from ..common import version
from ..specs.spec_repos import format_supported_course_list

ASSIGNMENT_REGEX = re.compile(r'^(HW|LAB|WS)', re.IGNORECASE)


def build_argparser():
    """Construct the argument list and parse the passed arguments"""
    parser = argparse.ArgumentParser(description='The core of the StoGrade toolkit')

    # Common arguments
    parser.add_argument('-v', '--version', action='store_true',
                        help='Print the version of the toolkit and exit')

    base_options = argparse.ArgumentParser(description='common options')
    base_options.add_argument('--skip-version-check', '-V', action='store_true',
                              default=os.getenv('STOGRADE_SKIP_VERSION_CHECK', False) is not False,
                              help='Skips the pypi update check')
    base_options.add_argument('--skip-dependency-check', action='store_true',
                              help='Skip checking for dependencies')
    base_options.add_argument('--skip-spec-update', '-S', action='store_true',
                              help='Skip checking for spec updates')
    base_options.add_argument('--debug', action='store_true',
                              help='Enable debugging mode (throw errors, implies -w1)')
    base_options.add_argument('--no-progress-bar', action='store_true',
                              help='Hide the progress bar')
    base_options.add_argument('--workers', '-w', type=int, default=os.cpu_count(), metavar='N',
                              help='The number of operations to perform in parallel')

    # Repository url modifiers
    repo_selection = argparse.ArgumentParser(add_help=False)
    repo_selection.add_argument('--course', default='', metavar='ID',
                                help='Which course to evaluate '
                                     '(this sets a default stogit url and downloads the correct specs). '
                                     'Can be {} or one of the previous with /f## or /s## (i.e. sd/s19)'
                                .format(format_supported_course_list(delimiter=', ')))
    repo_selection.add_argument('--stogit', metavar='URL',
                                help='Use an alternate stogit base URL (eg, git@stogit.cs.stolaf.edu:sd/s17)')

    # Recording options
    record_options = argparse.ArgumentParser(add_help=False)
    record_options.add_argument('--clean', action='store_true',
                                help='Remove student folders and re-clone them')
    record_options.add_argument('--skip-repo-update', '-R', action='store_true',
                                help='Do not update the student folders when checking')
    record_options.add_argument('--date', action='store', metavar='GIT_DATE',
                                help=('Check out last submission on GIT_DATE (eg, "last week", "tea time", "2 hrs ago")'
                                      '(see `man git-rev-list`)'))
    record_options.add_argument('--format', action='store', choices=['md', 'html'], default='md',
                                help='Set the output format')

    compile_options = argparse.ArgumentParser(add_help=False)
    compile_options.add_argument('--skip-web-compile', action='store_true',
                                 help='Skip compilation and testing of files marked with web: true')

    # Student selection
    student_selection = argparse.ArgumentParser(add_help=False)
    selection_args = student_selection.add_argument_group('student selection')
    selection_args.add_argument('--students', '--student', action='append', nargs='+', metavar='USERNAME', default=[],
                                help='Only iterate over these students.')
    selection_args.add_argument('--section', action='append', dest='sections', nargs='+', metavar='SECTION', default=[],
                                help='Only check these sections: my, all, a, b, etc.')

    # Table Printout Parent Parser
    table_options = argparse.ArgumentParser(add_help=False)
    table_options_args = table_options.add_argument_group('table printout options')
    table_options_args.add_argument('--sort', dest='sort_by', action='store', default='name', type=str,
                                    choices=['name', 'count'], help='Sort the students table')
    table_options_args.add_argument('--no-partials', '-P', action='store_true',
                                    help="Don't highlight partial submissions")

    # SubParsers
    sub_parsers = parser.add_subparsers(dest='command')

    # CI SubParser
    parser_ci = sub_parsers.add_parser('ci', parents=[base_options, compile_options], conflict_handler='resolve',
                                       help="Check a single student's assignment as part of a CI job")
    parser_ci.set_defaults(func=do_ci)

    # Drive SubParser
    parser_drive = sub_parsers.add_parser('drive', parents=[base_options, student_selection],
                                          conflict_handler='resolve', help='Manage submissions via google drive')
    parser_drive.set_defaults(func=do_drive)
    parser_drive.add_argument('assignments', nargs=1, metavar='HW',
                              help='An assignment to process')
    parser_drive.add_argument('--email', '-e', required=True,
                              help='Set the email of the group that documents are shared with '
                                   '(e.g. hd-tas@stolaf.edu)')

    # Record SubParser
    parser_record = sub_parsers.add_parser('record', help="Record students' work",
                                           parents=[base_options, record_options, compile_options,
                                                    repo_selection, table_options, student_selection],
                                           conflict_handler='resolve')
    parser_record.set_defaults(func=do_record)
    parser_record.add_argument('assignments', nargs='+', metavar='HW',
                               help='An assignment to process')
    parser_record.add_argument('--table', '-t', action='store_true',
                               help='Show the overview table after recording is complete')
    parser_record.add_argument('--gist', action='store_true',
                               help='Post overview table and student recordings as a private gist')
    parser_record.add_argument('--interact', action='store_true',
                               help="Interact with each student's submission individually")
    parser_record.add_argument('--skip-branch-check', '-B', action='store_true',
                               help='Do not check for unmerged branches')

    # Repo SubParser
    parser_repo = sub_parsers.add_parser('repo', help='Tools for cloning and updating student repositories',
                                         conflict_handler='resolve')
    repo_sub_parsers = parser_repo.add_subparsers()
    repo_sub_parsers.add_parser('clean', aliases=['reclone'], help='Remove and reclone student repositories',
                                parents=[base_options, repo_selection, student_selection],
                                conflict_handler='resolve').set_defaults(func=do_repo_clean)
    repo_sub_parsers.add_parser('update', aliases=['clone'], help='Clone and/or update student repos',
                                parents=[base_options, repo_selection, student_selection],
                                conflict_handler='resolve').set_defaults(func=do_repo_update)

    # Table SubParser
    parser_table = sub_parsers.add_parser('table', help='Print an table of the assignments submitted by students',
                                          parents=[base_options, record_options, compile_options, repo_selection,
                                                   table_options, student_selection],
                                          conflict_handler='resolve')
    parser_table.set_defaults(func=do_table)

    # Web SubParser
    parser_web = sub_parsers.add_parser('web', help='Run the CLI for grading React App files',
                                        parents=[base_options, record_options, compile_options,
                                                 repo_selection, student_selection],
                                        conflict_handler='resolve')
    parser_web.set_defaults(func=do_web)
    parser_web.add_argument('assignments', nargs=1, metavar='HW',
                            help='An assignment to process')
    parser_web.add_argument('--port', type=int, required=True,
                            help='Set the port for the server to use')

    return parser


def get_ci_assignments() -> List[str]:
    """Find assignments in the student's repository during a CI job"""
    all_assignments: List[str] = []
    dirs = glob('hw*') + glob('lab*') + glob('ws*')
    for line in dirs:
        all_assignments.append(line.split('/')[-1])
    return natsorted(set(all_assignments))


def process_args() -> Tuple[Dict[str, Any], List[str], List[str]]:
    """Process the arguments and create usable data from them"""
    parser = build_argparser()
    args = vars(parser.parse_args())

    if args['version']:
        print('version', version)
        sys.exit(0)

    global_vars.DEBUG = args.get('debug', False)
    logging.basicConfig(level=logging.DEBUG if global_vars.DEBUG else logging.WARNING)

    command: str = args['command']

    # ci SubCommand
    if command == 'ci':
        assignments = get_ci_assignments()
        students = [os.environ['CI_PROJECT_NAME']]
        args['course'] = os.environ['CI_PROJECT_NAMESPACE']
        global_vars.CI = True

    # record SubCommand
    elif command == 'record':
        assignments = natsorted(set(args['assignments']))  # Has at least one assignment (enforced by argparser)
        students = get_students(args)

    # table SubCommand
    elif command == 'table':
        assignments = []  # Will be filled in later once we know that the data/specs directory exists
        students = get_students(args)

    # web SubCommand
    elif command == 'web':
        assignments = natsorted(set(args['assignments']))  # Has only one assignment (enforced by argparser)
        students = get_students(args)

    # repo SubCommand
    elif command == 'repo':
        assignments = []
        students = get_students(args)

    elif command == 'drive':
        assignments = natsorted(set(args['assignments']))
        students = get_students(args)
        args['course'] = ''

    else:
        print('Sub-command must be specified', file=sys.stderr)
        sys.exit(1)

    if not students:
        print('No students selected', file=sys.stderr)
        print('Is your students.txt missing?', file=sys.stderr)
        sys.exit(1)

    debug_print_args(args)
    debug_print_students(students)
    debug_print_assignments(assignments)

    return args, students, assignments


def debug_print_args(args: Dict[str, Any]):
    logging.debug("Command Line Arguments:")
    for arg, value in args.items():
        logging.debug("{}: {}".format(arg, str(value)))


def debug_print_students(students: List[str]):
    logging.debug("Students:")
    debug_print_grid(students)


def debug_print_assignments(assignments: List[str]):
    logging.debug("Assignments:")
    debug_print_grid(assignments)


def debug_print_grid(items: List[str]):
    line = ""
    for i, item in enumerate(items):
        line += item.ljust(10)
        if i % 5 == 4 or i == len(items) - 1:
            logging.debug(line)
            line = ""
