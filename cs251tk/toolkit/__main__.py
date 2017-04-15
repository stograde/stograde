import functools
import logging
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from os import makedirs, getcwd
import os.path

from ..common import chdir
from ..specs import load_all_specs, check_dependencies
from .find_update import update_available
from .process_student import process_student
from .args import process_args
from .progress_bar import progress_bar
from .save_recordings import save_recordings, gist_recordings
from .tabulate import tabulate


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
        msg = ', '.join(sorted(remaining))
        progress_bar(size, invocation_count, message=msg)

    msg = ', '.join(sorted(remaining))
    progress_bar(size, invocation_count, message=msg)
    return increment


def main():
    basedir = getcwd()

    args, usernames, assignments, stogit_url = process_args()
    clean = args['clean']
    date = args['date']
    debug = args['debug']
    gist = args['gist']
    highlight_partials = args['highlight_partials']
    interact = args['interact']
    no_check = args['no_check']
    no_update = args['no_update']
    no_progress = args['no_progress']
    quiet = args['quiet']
    skip_update_check = args['skip_update_check']
    sort_by = args['sort_by']
    workers = args['workers']

    if debug:
        workers = 1
    if interact:
        workers = 1

    current_version, new_version = update_available(skip_update_check=skip_update_check)
    if new_version:
        print((
            'v{} is available: you have v{}. '
            'Try "pip3 install --no-cache --user --update cs251tk" '
            'to update.'
        ).format(current_version, new_version))

    logging.basicConfig(level=logging.DEBUG if debug else logging.WARNING)

    if date:
        logging.debug('Checking out {}'.format(date))

    specs = load_all_specs(basedir=os.path.join(basedir, 'data'))
    if not specs:
        print('no specs loaded!')
        sys.exit(1)

    for spec_to_use in assignments:
        check_dependencies(specs[spec_to_use])

    results = []
    records = []
    makedirs('./students', exist_ok=True)
    with chdir('./students'):
        single = functools.partial(
            process_student,
            assignments=assignments,
            basedir=basedir,
            clean=clean,
            date=date,
            debug=debug,
            interact=interact,
            no_check=no_check,
            no_update=no_update,
            specs=specs,
            stogit_url=stogit_url
        )

        if workers > 1:
            print_progress = make_progress_bar(usernames, no_progress=no_progress)
            with ProcessPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(single, name) for name in usernames]
                for future in as_completed(futures):
                    result, recording = future.result()
                    print_progress(result['username'])
                    results.append(result)
                    records.extend(recording)

        else:
            for student in usernames:
                print('processing {}'.format(student))
                result, recording = single(student)
                results.append(result)
                records.extend(recording)

    if not quiet:
        table = tabulate(results, sort_by=sort_by, highlight_partials=highlight_partials)
        print('\n' + table)

    if gist:
        table = tabulate(results, sort_by=sort_by, highlight_partials=highlight_partials)
        gist_recordings(records, table, debug=debug)
    else:
        save_recordings(records, debug=debug)
