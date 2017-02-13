"""Deal with argument parsing for the toolkit"""

import argparse
import textwrap
import re
from os import cpu_count
from logging import warning
from natsort import natsorted

from cs251tk.common import flatten
from .get_students import get_students

ASSIGNMENT_REGEX = re.compile(r'^(HW|LAB)', re.IGNORECASE)


def get_args():
    """Construct the argument list and parse the passed arguments"""
    parser = argparse.ArgumentParser(description='The core of the CS251 toolkit')
    parser.add_argument('input', nargs='*',
                        help='A mixed list of students and assignments')
    parser.add_argument('--debug', action='store_true',
                        help='enable debugging mode (throw errors, implies -w1)')

    selection = parser.add_argument_group('student-selection arguments')
    selection.add_argument('--students', action='append', nargs='+', metavar='USERNAME', default=[],
                           help='Only iterate over these students.')
    selection.add_argument('--section', action='append', nargs='+', metavar='SECTION', default=[],
                           help='Only check these sections: my, all, a, b, etc')
    selection.add_argument('--all', '-a', action='store_true',
                           help='Shorthand for \'--section all\'')

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--quiet', '-q', action='store_true',
                          help='Don\'t show the table')
    optional.add_argument('--no-progress', action='store_true',
                          help='Hide the progress bar')
    optional.add_argument('--workers', '-w', type=int, default=cpu_count(), metavar='N',
                          help='The number of operations to perform in parallel')
    optional.add_argument('--sort', action='store', default='name', type=str,
                          choices=['name', 'count'],
                          help='Sort the students table')
    optional.add_argument('--partials', '-p', action='store_true',
                          help='Highlight partial submissions')

    folder = parser.add_argument_group('student management arguments')
    folder.add_argument('--clean', action='store_true',
                        help='Remove student folders and re-clone them')
    folder.add_argument('--no-update', '-n', action='store_true',
                        help='Do not update the student folders when checking')
    folder.add_argument('--stogit', metavar='URL',
                        default='git@stogit.cs.stolaf.edu:sd-s17',
                        help='Use an alternate stogit base URL')

    dates = parser.add_argument_group('time-based arguments')
    dates.add_argument('--date', action='store', metavar='GIT_DATE',
                       help='Check out last submission on GIT_DATE (eg, "last week", "tea time", "2 hrs ago") (see `man git-rev-list`)')

    grading = parser.add_argument_group('grading arguments')
    grading.add_argument('--no-check', '-c', action='store_true',
                         help='Do not check for unmerged branches')
    grading.add_argument('--record', action='append', nargs='+', metavar='HW', default=[],
                         help='Record information on student submissions. Requires a spec file')
    grading.add_argument('--gist', action='store_true',
                         help='Post overview table and student recordings as a private gist')

    return parser


def massage_args(args, students):
    assignments = [l for l in args['input'] if re.match(ASSIGNMENT_REGEX, l)]
    people = [l for l in args['input'] if not re.match(ASSIGNMENT_REGEX, l)]

    # argparser puts it into a nested list because you could have two
    # occurrences of the arg, each with a variable number of arguments.
    # `--students amy max --students rives` becomes `[[amy, max], [rives]]`
    args['students'] = list(flatten(args['students'])) + people
    args['section'] = list(flatten(args['section']))
    args['record'] = natsorted(set(list(flatten(args['record'])) + assignments))

    if args['all']:
        args['section'] = ['all']

    # fall back to the students.my section
    if not args['students'] and not args['section']:
        args['section'] = ['my']

    # support 'my' students and 'all' students
    if 'my' in args['section']:
        if 'my' not in students:
            warning('There is no [my] section in students.txt')
            return args
        args['students'] = students['my']

    elif 'all' in args['section']:
        sections = [students[section] for section in students]
        args['students'] = list(flatten(sections))

    # sections are identified by only being one char long
    elif args['section']:
        sections = []
        for section in args['section']:
            try:
                sections.append(students['section-' + section] or students[section])
            except KeyError:
                warning('Section "{}" could not be found in ./students.txt'.format(section))
        args['students'] = list(flatten(sections))

    # stop if we still don't have any students
    if not args['students']:
        msg = textwrap.dedent("""
            Could not find a list of students. You must provide the
            `--students` argument, the `--section` argument, or a
            ./students.txt file.
        """)
        warning(textwrap.fill(msg))
        return args

    # sort students and remove any duplicates
    args['students'] = sorted(set(args['students']))

    return args


def process_args():
    """Process the arguments and create usable data from them"""
    parser = get_args()
    args = vars(parser.parse_args())
    students = get_students()
    return massage_args(args, students)
