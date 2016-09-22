import functools
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from os import makedirs, getcwd

from cs251tk.common import chdir
from cs251tk.toolkit import process_student
from cs251tk.toolkit import process_args
from cs251tk.toolkit import progress_bar
from cs251tk.toolkit import save_recordings
from cs251tk.toolkit import tabulate
from cs251tk.specs import load_all_specs


def make_progress_bar(students, no_progress=False):
    if no_progress:
        return lambda _: None

    size = len(students)
    remaining = set(students)
    invocation_count = 0

    def increment(username):
        nonlocal remaining
        nonlocal invocation_count
        remaining.remove(username)
        invocation_count += 1
        msg = ', '.join(remaining)
        progress_bar(size, invocation_count, message=msg)

    msg = ', '.join(remaining)
    progress_bar(size, invocation_count, message=msg)
    return increment


def main():
    args = process_args()
    basedir = getcwd()
    # check_for_updates()

    if args['day']:
        print('Checking out {} at 5:00pm'.format(args['day']))

    specs = load_all_specs()
    if not specs:
        print('no specs loaded!')
        sys.exit(1)

    print_progress = make_progress_bar(args['students'])

    results = []
    records = []
    makedirs('./students', exist_ok=True)
    with chdir('./students'):
        single = functools.partial(process_student, args=args, specs=specs, basedir=basedir)

        if args['workers'] > 1:
            with ProcessPoolExecutor(max_workers=args['workers']) as pool:
                futures = [pool.submit(single, student) for student in args['students']]
                for future in as_completed(futures):
                    result, recording = future.result()
                    print_progress(result['username'])
                    results.append(result)
                    records.append(recording)

        else:
            for student in args['students']:
                result, recording = single(student)
                print_progress(result['username'])
                results.append(result)
                records.append(recording)

    table = tabulate(results, sort_by=args['sort'], partials=args['partials'])
    if not args['quiet']:
        print('\n' + table)

    save_recordings(records, table, destination='gist' if args['gist'] else 'file')
