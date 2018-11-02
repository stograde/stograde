"""Deal with argument parsing for the toolkit"""

import datetime
import argparse
import sys
import re
from os import cpu_count, getenv
from logging import warning
from natsort import natsorted
from typing import List

from cs251tk.common import flatten, version
from .get_students import get_students as load_students_from_file

ASSIGNMENT_REGEX = re.compile(r'^(HW|LAB)', re.IGNORECASE)


def build_argparser():
    """Construct the argument list and parse the passed arguments"""
    parser = argparse.ArgumentParser(description='The core of the CS251 toolkit')
    parser.add_argument('input_items', nargs='*', metavar='ITEM',
                        help='A mixed list of students and assignments')
    parser.add_argument('-v', '--version', action='store_true',
                        help='print the version of the toolkit')
    parser.add_argument('--debug', action='store_true',
                        help='enable debugging mode (throw errors, implies -w1)')
    parser.add_argument('--skip-update-check', action='store_true',
                        default=getenv('CS251TK_SKIP_UPDATE_CHECK', False) is not False,
                        help='skips the pypi update check')

    specs = parser.add_argument_group('control the homework specs')
    specs.add_argument('--course', default='sd', choices=['sd', 'hd'],
                       help='Which course to evaluate (this sets a default stogit url)')

    selection = parser.add_argument_group('student-selection arguments')
    selection.add_argument('--students', action='append', nargs='+', metavar='USERNAME', default=[],
                           help='Only iterate over these students.')
    selection.add_argument('--section', action='append', dest='sections', nargs='+', metavar='SECTION', default=[],
                           help='Only check these sections: my, all, a, b, etc')
    selection.add_argument('--all', '-a', dest='all_sections', action='store_true',
                           help='Shorthand for \'--section all\'')

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--quiet', '-q', action='store_true',
                          help="Don't show the table")
    optional.add_argument('--no-progress', action='store_true',
                          help='Hide the progress bar')
    optional.add_argument('--workers', '-w', type=int, default=cpu_count(), metavar='N',
                          help='The number of operations to perform in parallel')
    optional.add_argument('--sort', dest='sort_by', action='store', default='name', type=str,
                          choices=['name', 'count'],
                          help='Sort the students table')
    optional.add_argument('--partials', '-p', dest='highlight_partials', action='store_true',
                          help='Highlight partial submissions')

    folder = parser.add_argument_group('student management arguments')
    folder.add_argument('--clean', action='store_true',
                        help='Remove student folders and re-clone them')
    folder.add_argument('--no-update', '-n', action='store_true',
                        help='Do not update the student folders when checking')
    folder.add_argument('--stogit', metavar='URL',
                        help='Use an alternate stogit base URL (eg, git@stogit.cs.stolaf.edu:sd-s17)')

    dates = parser.add_argument_group('time-based arguments')
    dates.add_argument('--date', action='store', metavar='GIT_DATE',
                       help=('Check out last submission on GIT_DATE (eg, "last week", "tea time", "2 hrs ago")'
                             '(see `man git-rev-list`)'))

    grading = parser.add_argument_group('grading arguments')
    grading.add_argument('--no-check', '-c', action='store_true',
                         help='Do not check for unmerged branches')
    grading.add_argument('--record', dest='to_record', action='append', nargs='+', metavar='HW', default=[],
                         help='Record information on student submissions. Requires a spec file')
    grading.add_argument('--gist', action='store_true',
                         help='Post overview table and student recordings as a private gist')
    grading.add_argument('--interact', action='store_true',
                         help="Interact with each student's submission individually")

    return parser


def get_students_from_args(*, input_items, all_sections, sections, students, _all_students, **kwargs) -> List[str]:
    people = [l for l in input_items if not re.match(ASSIGNMENT_REGEX, l)]

    # argparser puts it into a nested list because you could have two
    # occurrences of the arg, each with a variable number of arguments.
    # `--students amy max --students rives` becomes `[[amy, max], [rives]]`
    people = [student for group in students for student in group] + people
    sections = [sect for group in sections for sect in group]

    if all_sections:
        sections = ['all']

    # fall back to the students.my section
    if not people and not sections:
        sections = ['my']

    # support 'my' students and 'all' students
    if 'my' in sections:
        if 'my' not in _all_students:
            warning('There is no [my] section in students.txt')
            return sorted(set(people))
        people = _all_students['my']

    elif 'all' in sections:
        people = list(flatten([_all_students[section] for section in _all_students]))

    # sections are identified by only being one char long
    elif sections:
        collected = []
        for section_name in sections:
            student_set = []
            prefixed = 'section-{}'.format(section_name)

            if section_name in _all_students:
                student_set = _all_students[section_name]
            elif prefixed in _all_students:
                student_set = _all_students[prefixed]
            else:
                warning((
                    'Neither section [section-{0}] nor [{0}] '
                    'could not be found in ./students.txt'
                ).format(section_name))

            collected.append(student_set)
        people = [student for group in collected for student in group]

    # sort students and remove any duplicates
    return sorted(set(people))


def get_assignments_from_args(*, input_items, to_record, **kwargs) -> List[str]:
    # grab the assignments given on the plain args list
    assignments = [l for l in input_items if re.match(ASSIGNMENT_REGEX, l)]

    # argparser puts --record into a nested list because you could have two
    # occurrences of the arg, each with a variable number of arguments.
    # `--record hw4 lab1 --record hw5` becomes `[[hw4, lab1], [hw5]]`
    assignments = [assignment for group in to_record for assignment in group] + assignments

    # sort the assignments and remove duplicates
    return natsorted(set(assignments))


def compute_stogit_url(*, stogit, course, _now, **kwargs) -> str:
    """calculate a default stogit URL, or use the specified one"""
    if stogit:
        return stogit

    semester = 's' if _now.month < 7 else 'f'
    year = str(_now.year)[2:]
    return 'git@stogit.cs.stolaf.edu:{}-{}{}'.format(course, semester, year)


def process_args():
    """Process the arguments and create usable data from them"""
    parser = build_argparser()
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['version']:
        print('version', version)
        sys.exit(0)

    students = get_students_from_args(**args, _all_students=load_students_from_file())
    assignments = get_assignments_from_args(**args)
    stogit = compute_stogit_url(**args, _now=datetime.date.today())

    if debug:
        print_args(args)
        print(file=sys.stderr)
        print_students(students)
        print(file=sys.stderr)
        print_assignments(assignments)
        print(file=sys.stderr)
        print("stogit URL: " + stogit, file=sys.stderr)
        print(file=sys.stderr)

    return args, students, assignments, stogit


def print_args(args):
    print("Command Line Arguments:", file=sys.stderr)
    print("input_items:\t\t" + str(args['input_items']), file=sys.stderr)
    print("version:\t\t" + str(args['version']), file=sys.stderr)
    print("debug:\t\t\t" + str(args['debug']), file=sys.stderr)
    print("skip_update_check:\t" + str(args['skip_update_check']), file=sys.stderr)
    print("course:\t\t\t" + str(args['course']), file=sys.stderr)
    print("students:\t\t" + str(args['students']), file=sys.stderr)
    print("sections:\t\t" + str(args['sections']), file=sys.stderr)
    print("all_sections:\t\t" + str(args['all_sections']), file=sys.stderr)
    print("quiet:\t\t\t" + str(args['quiet']), file=sys.stderr)
    print("no_progress:\t\t" + str(args['no_progress']), file=sys.stderr)
    print("workers:\t\t" + str(args['workers']), file=sys.stderr)
    print("sort_by:\t\t" + str(args['sort_by']), file=sys.stderr)
    print("highlight_partials:\t" + str(args['highlight_partials']), file=sys.stderr)
    print("clean:\t\t\t" + str(args['clean']), file=sys.stderr)
    print("no_update:\t\t" + str(args['no_update']), file=sys.stderr)
    print("stogit:\t\t\t" + str(args['stogit']), file=sys.stderr)
    print("date:\t\t\t" + str(args['date']), file=sys.stderr)
    print("no_check:\t\t" + str(args['no_check']), file=sys.stderr)
    print("to_record:\t\t" + str(args['to_record']), file=sys.stderr)
    print("gist:\t\t\t" + str(args['gist']), file=sys.stderr)
    print("interact:\t\t" + str(args['interact']), file=sys.stderr)


def print_assignments(args):
    print("Assignments:", file=sys.stderr)
    count = 0
    for arg in args:
        if count % 5 == 4:
            print(arg, file=sys.stderr)
        else:
            print(arg, end="", file=sys.stderr)
            for i in range(arg.__len__(), 8):
                print(end=" ", file=sys.stderr)
        count += 1
    print(file=sys.stderr)


def print_students(students):
    print("Students:", file=sys.stderr)
    count = 0
    for student in students:
        if count % 5 == 4:
            print(student, file=sys.stderr)
        else:
            print(student, end="", file=sys.stderr)
            for i in range(student.__len__(), 10):
                print(end=" ", file=sys.stderr)
        count += 1
