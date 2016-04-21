#!/usr/bin/env python3
from concurrent.futures import ProcessPoolExecutor
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


def main():
    check_for_updates()
    args = process_args()

    if args['day']:
        print('Checking out %s at 5:00pm' % args['day'])

    recording_files = {}
    if args['record']:
        recording_files = {to_record: open('logs/log-%s.md' % to_record, 'w', encoding='utf-8')
                           for to_record in args['record']}

    specs = load_specs()
    results = []
    makedirs('./students', exist_ok=True)
    with chdir('./students'):
        try:
            def progress(i, student):
                if args['no_progress']:
                    return
                progress_bar(len(args['students']), i, message='%s' % student)

            single = functools.partial(single_student, args=args, specs=specs)

            # start the progress bar!
            students_left = set(args['students'])
            progress(0, ', '.join(students_left))

            if args['workers'] > 1:
                with ProcessPoolExecutor(max_workers=args['workers']) as pool:
                    jobs = pool.map(single, args['students'])
                for i, (result, records) in enumerate(jobs):
                    students_left.remove(result['username'])
                    progress(i+1, ', '.join(students_left))
                    results.append(result)
                    save_recordings(records, recording_files)

            else:
                jobs = map(single, args['students'])
                for i, (result, records) in enumerate(jobs):
                    students_left.remove(result['username'])
                    progress(i+1, ', '.join(students_left))
                    results.append(result)
                    save_recordings(records, recording_files)

        finally:
            [recording.close() for recording in recording_files.values()]

    if not args['quiet']:
        print('\n' + tabulate(results, sort_by=args['sort']))


if __name__ == '__main__':
    main()
