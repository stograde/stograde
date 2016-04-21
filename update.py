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

    remaining = set(students)
    invocation_count = 0

    progress_bar(len(students), invocation_count, message=', '.join(remaining))

    def increment(username):
        nonlocal remaining
        nonlocal invocation_count
        remaining.remove(username)
        invocation_count += 1
        msg = ', '.join(remaining)
        progress_bar(len(students), invocation_count, message=', '.join(remaining))

    return increment


def open_recording_files(to_record):
    if to_record:
        return {file: open('logs/log-{}.md'.format(file), 'w', encoding='utf-8')
                for file in to_record}
    return {}


def main():
    check_for_updates()
    args = process_args()

    if args['day']:
        print('Checking out %s at 5:00pm' % args['day'])

    print_progress = make_progress_bar(args['students'])
    recording_files = open_recording_files(args['record'])
    specs = load_specs()
    results = []

    makedirs('./students', exist_ok=True)
    with chdir('./students'):
        try:
            single = functools.partial(single_student, args=args, specs=specs)

            if args['workers'] > 1:
                with ProcessPoolExecutor(max_workers=args['workers']) as pool:
                    futures = [pool.submit(single, student) for student in args['students']]
                    for future in as_completed(futures):
                        result, records = future.result()
                        print_progress(result['username'])
                        results.append(result)
                        save_recordings(records, recording_files)

            else:
                for (result, records) in map(single, args['students']):
                    print_progress(result['username'])
                    results.append(result)
                    save_recordings(records, recording_files)

        finally:
            [recording.close() for recording in recording_files.values()]

    if not args['quiet']:
        print('\n' + tabulate(results, sort_by=args['sort']))


if __name__ == '__main__':
    main()
