#!/usr/bin/env python3
from concurrent.futures import ProcessPoolExecutor, as_completed
from os import makedirs
import functools

from lib import check_for_updates
from lib import save_recordings
from lib import single_student
from lib import progress_bar
from lib import process_args
from lib import load_specs
from lib import tabulate
from lib import chdir


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
        progress_bar(size, invocation_count, message=', '.join(remaining))

    progress_bar(size, invocation_count, message=', '.join(remaining))
    return increment


def main():
    check_for_updates()
    args = process_args()

    if args['day']:
        print('Checking out {} at 5:00pm'.format(args['day']))

    specs = load_specs()

    print_progress = make_progress_bar(args['students'])

    results = []
    records = []
    makedirs('./students', exist_ok=True)
    with chdir('./students'):
        single = functools.partial(single_student, args=args, specs=specs)

        if args['workers'] > 1:
            with ProcessPoolExecutor(max_workers=args['workers']) as pool:
                futures = [pool.submit(single, student) for student in args['students']]
                for future in as_completed(futures):
                    result, recording = future.result()
                    print_progress(result['username'])
                    results.append(result)
                    records.append(recording)

        else:
            for (result, recording) in map(single, args['students']):
                print_progress(result['username'])
                results.append(result)
                records.append(recording)

    table = tabulate(results, sort_by=args['sort'], partials=args['partials'])
    if not args['quiet']:
        print('\n' + table)

    save_recordings(records, table)


if __name__ == '__main__':
    main()
