import argparse
import textwrap
from .warn import warn
from .flatten import flatten
from .get_students import get_students


def get_args():
    parser = argparse.ArgumentParser(description='The core of the CS251 toolkit.')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Be quieter')
    parser.add_argument('--no-progress', action='store_true',
                        help='Hide the progress bar')
    parser.add_argument('--no-update', '-n', action='store_true',
                        help='Do not update the student folders before checking.')
    parser.add_argument('--no-check', '-c', action='store_true',
                        help='Do not check for unmerged branches.')
    parser.add_argument('--day', action='store',
                        help='Check out the student folder as of 5pm on the last <day of week>.')
    parser.add_argument('--date', action='store',
                        help='Check out the student folder as of 5pm on <date> (Y-M-D).')
    parser.add_argument('--clean', action='store_true',
                        help='Remove student folders and re-clone them')
    parser.add_argument('--record', action='append', nargs='+', metavar='HW',
                        help="Record information on student submissions. Requires a spec file.")
    parser.add_argument('--students', action='append', nargs='+', metavar='STUDENT',
                        help='Only iterate over these students.')
    parser.add_argument('--section', action='append', nargs='+', metavar='SECTION',
                        help='Only check these sections: my, all, a, b, etc.')
    parser.add_argument('--sort-by', action='store', default='name', type=str,
                        choices=['name', 'homework'],
                        help='Sort by either student name or homework count.')
    parser.add_argument('--all', action='store_true',
                        help='Shorthand for \'--section all\'')
    parser.add_argument('--workers', '-w', type=int, default=4,
                        help='Control the number of operations to perform in parallel')
    return vars(parser.parse_args())


def process_args():
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
        args['students'] = flatten(args['students'] + sys.stdin.read().splitlines())
        args['students'] = [student for student in args['students'] if student != '-']

    elif '-' in args['record']:
        args['record'] = flatten(args['record'] + sys.stdin.read().splitlines())
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
