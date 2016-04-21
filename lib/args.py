'''Deal with argument parsing for the toolkit'''

import argparse
import textwrap
from sys import stdin
from os import cpu_count
from .helpers import warn
from .helpers import flatten
from .get_students import get_students
from .run import run


def get_args():
    '''Construct the argument list and parse the passed arguments'''
    parser = argparse.ArgumentParser(description='The core of the CS251 toolkit')

    selection = parser.add_argument_group('student-selection arguments')
    selection.add_argument('--students', action='append', nargs='+', metavar='USERNAME',
                           help='Only iterate over these students.')
    selection.add_argument('--section', action='append', nargs='+', metavar='SECTION',
                           help='Only check these sections: my, all, a, b, etc')
    selection.add_argument('--all', action='store_true',
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

    folder = parser.add_argument_group('student-folder arguments')
    folder.add_argument('--clean', action='store_true',
                        help='Remove student folders and re-clone them')
    folder.add_argument('--no-update', '-n', action='store_true',
                        help='Do not update the student folders when checking')

    dates = parser.add_argument_group('time-based arguments')
    dates.add_argument('--day', action='store',
                       choices=['sun', 'mon', 'tues', 'wed', 'thurs', 'fri', 'sat'],
                       help='Check out submissions as of 5pm on WEEKDAY')
    dates.add_argument('--date', action='store', metavar='YYYY-MM-DD',
                       help='Check out submissions as of 5pm on DATE')

    grading = parser.add_argument_group('grading arguments')
    grading.add_argument('--no-check', '-c', action='store_true',
                         help='Do not check for unmerged branches')
    grading.add_argument('--record', action='append', nargs='+', metavar='HW',
                         help='Record information on student submissions. Requires a spec file')

    return vars(parser.parse_args())


def process_args():
    '''Process the arguments and create usable data from them'''
    students = get_students()
    args = get_args()

    # argparser puts it into a nested list because you could have two
    # occurrences of the arg, each with a variable number of arguments.
    # `--students amy max --students rives` => `[[amy, max], [rives]]`
    args['students'] = list(flatten(args['students'] or []))
    args['section'] = list(flatten(args['section'] or []))
    args['record'] = list(flatten(args['record'] or []))

    if args['all']:
        args['section'] = ['all']

    # fall back to the students.my section
    if not args['students'] and not args['section']:
        args['section'] = ['my']

    # support 'my' students and 'all' students
    if 'my' in args['section']:
        if 'my' not in students:
            warn('There is no [my] section in students.txt')
            return
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
                warn('Section "%s" could not be found in ./students.txt' % section)
        args['students'] = list(flatten(sections))

    # we can only read one stdin
    if '-' in args['students']:
        args['students'] = flatten(args['students'] + stdin.read().splitlines())
        args['students'] = [student for student in args['students'] if student != '-']

    elif '-' in args['record']:
        args['record'] = flatten(args['record'] + stdin.read().splitlines())
        args['record'] = [to_record for to_record in args['record'] if to_record != '-']

    # stop if we still don't have any students
    if not args['students']:
        msg = textwrap.dedent('''
            Could not find a list of students.
            You must provide the `--students` argument, the `--section` argument,
            a ./students.txt file, or a list of usernames to stdin.
        ''')
        warn(textwrap.fill(msg))
        return

    args['students'] = sorted(set(args['students']))

    if args['day']:
        _, args['day'] = run(['date', '-v1w', '-v-' + args['day'], '+%Y-%m-%d'])
    elif args['date']:
        args['day'] = args['date']

    return args
