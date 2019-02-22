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


def download_specs(course, basedir, stogit):
    spec_urls = {
        'sd': 'https://github.com/StoDevX/cs251-specs.git',
        'hd': 'https://github.com/StoDevX/cs241-specs.git',
        'ads': 'https://github.com/Jedmeyer/cs253-specs.git'
    }
    course = course.split("-")[0].lower()
    try:
        url = spec_urls[course]
    except KeyError:
        print("Course {} not recognized".format(course))
        sys.exit(1)
    with chdir(basedir):
        run(['git', 'clone', url, 'data'])
        if not stogit:
            return compute_stogit_url(course=course, stogit=None, _now=datetime.date.today())


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
        if args['ci']:
            if args['course']:
                url = download_specs(args['course'], basedir, args['stogit'])
                if not args['stogit']:
                    stogit_url = url
            else:
                print("data directory not found and no course specified")
                sys.exit(1)

        else:
            print('data directory not found', file=sys.stderr)
            if args['course']:
                download = input("Download specs for {}? (Y/N)".format(args['course'].upper()))
                if download and download.lower()[0] == "y":
                    url = download_specs(args['course'], basedir, args['stogit'])
                    if not args['stogit']:
                        stogit_url = url
                else:
                    sys.exit(1)
            else:
                download = input("Download specs? (Y/N)")
                if download and download.lower()[0] == "y":
                    repo = input("Which class? (SD/HD/ADS)")
                    if repo:
                        url = download_specs(repo, basedir, args['stogit'])
                        if not args['stogit']:
                            stogit_url = url
                    else:
                        sys.exit(1)
                else:
                    sys.exit(1)

    specs = load_all_specs(basedir=os.path.join(basedir, 'data'), skip_update_check=skip_update_check)
    if not specs:
        print('no specs loaded!')
        sys.exit(1)

    if assignments:
        available_specs = set(assignments)

        for spec_to_use in assignments:
            try:
                check_dependencies(specs[spec_to_use])
            except KeyError:
                print('Spec {} does not exist'.format(spec_to_use), file=sys.stderr)
                available_specs.remove(spec_to_use)

        assignments = available_specs

        if not assignments:
            print('no valid specs remaining', file=sys.stderr)
            sys.exit(1)

    results = []
    records = []
    if not ci:
        makedirs('./students', exist_ok=True)
    directory = './students' if not ci else '.'
    with chdir(directory):
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
            web=web
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

    if ci or not quiet:
        table = tabulate(results, sort_by=sort_by, highlight_partials=highlight_partials)
        if ci:
            print(table + '\n')
        elif not quiet:
            print('\n' + table)

    if gist:
        table = tabulate(results, sort_by=sort_by, highlight_partials=highlight_partials)
        gist_recordings(records, table, debug=debug)
    elif ci:
        failure = False
        for record in records:
            for file in record['files']:
                # Alert student about any missing files
                if record['files'][file]['missing']:
                    logging.error("{}: File {} missing".format(record['spec'], record['files'][file]['filename']))
                    failure = True
                else:
                    # Alert student about any compilation errors
                    for compilation in record['files'][file]['compilation']:
                        if compilation['status'] != 'success':
                            logging.error("{}: File {} compile error:\n\n\t{}"
                                          .format(record['spec'], record['files'][file]['filename'],
                                                  compilation['output'].replace("\n", "\n\t")))
                            failure = True
        if failure:
            sys.exit(1)
    else:
        save_recordings(records, debug=debug)
