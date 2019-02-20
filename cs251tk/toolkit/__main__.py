import datetime
import functools
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from threading import Thread
from os import makedirs, getcwd
import os.path
import logging

from ..common import chdir, run
from ..specs import load_all_specs, check_dependencies
from .find_update import update_available
from .process_student import process_student
from .args import process_args, compute_stogit_url
from .progress_bar import progress_bar
from .save_recordings import save_recordings, gist_recordings
from .tabulate import tabulate
from ..webapp import server


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


def run_server(basedir):
    server.exe_name = '"{}/server/server_file"'.format(basedir)
    server.run_server()
    return


def main():
    basedir = getcwd()
    args, usernames, assignments, stogit_url = process_args()
    ci = args['ci']
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
    web = args['web']
    workers = args['workers']

    if debug or interact or web:
        workers = 1

    current_version, new_version = update_available(skip_update_check=skip_update_check)
    if new_version:
        print(('v{} is available: you have v{}. '
               'Try "pip3 install --no-cache --user --upgrade cs251tk" '
               'to update.').format(new_version, current_version), file=sys.stderr)

    if date:
        logging.debug('Checking out {}'.format(date))

    if not os.path.exists("data"):
        print('data directory not found', file=sys.stderr)
        download = input("Download specs? (Y/N)")
        if download and download.lower()[0] == "y":
            repo = input("Which class? (SD/HD)")
            if repo and repo.lower()[0] == 's':
                with chdir(basedir):
                    run(['git', 'clone', 'https://github.com/StoDevX/cs251-specs.git', 'data'])
                    if not args['stogit']:
                        stogit_url = compute_stogit_url(course="sd", stogit=None, _now=datetime.date.today())
            elif repo and repo.lower()[0] == "h":
                with chdir(basedir):
                    run(['git', 'clone', 'https://github.com/StoDevX/cs241-specs.git', 'data'])
                    if not args['stogit']:
                        stogit_url = compute_stogit_url(course="hd", stogit=None, _now=datetime.date.today())
            else:
                print("Class not recognized", file=sys.stderr)
                sys.exit(1)
        else:
            sys.exit(1)

    specs = load_all_specs(basedir=os.path.join(basedir, 'data'), skip_update_check=skip_update_check)
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
            stogit_url=stogit_url,
            ci=ci
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
        elif web:
            Thread(target=run_server, args=(basedir,), daemon=True).start()
            for student in usernames:
                print("\nStudent: {}".format(student))
                result, recording = single(student)
                results.append(result)
                records.extend(recording)
        else:
            for student in usernames:
                logging.debug('Processing {}'.format(student))
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
