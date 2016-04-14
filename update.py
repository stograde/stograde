#!/usr/bin/env python3
from concurrent.futures import ProcessPoolExecutor
from os import getcwd, makedirs
import functools

from os import path
from lib import check_for_updates
from lib import save_recordings
from lib import single_student
from lib import progress_bar
from lib import process_args
from lib import columnize
from lib import chdir
from lib import size
from lib import yaml
from lib import run


def main():
    check_for_updates()
    args = process_args()

    if args['day']:
        print('Checking out %s at 5:00pm' % args['day'])

    table_rows = []
    recording_files = {}
    specs = {}
    if args['record']:
        for to_record in args['record']:
            spec_filename = path.join('specs', to_record + '.yaml')
            log_filename = path.join('logs', 'log-' + to_record + '.md')

            recording_files[to_record] = open(log_filename, 'w', encoding='utf-8')
            with open(spec_filename, 'r', encoding='utf-8') as specfile:
                spec = specfile.read()
                if spec:
                    specs[to_record] = yaml.safe_load(spec)

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
                for i, (student, row, records) in enumerate(jobs):
                    students_left.remove(student)
                    progress(i+1, ', '.join(students_left))
                    table_rows.append(row)
                    save_recordings(records, recording_files)

            else:
                jobs = map(single, args['students'])
                for i, (student, row, records) in enumerate(jobs):
                    students_left.remove(student)
                    progress(i+1, ', '.join(students_left))
                    table_rows.append(row)
                    save_recordings(records, recording_files)

        finally:
            [recording.close() for recording in recording_files.values()]

    if not args['quiet']:
        print('\n' + columnize(table_rows, sort_by=args['sort_by']))


if __name__ == '__main__':
    main()
