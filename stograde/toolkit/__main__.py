import datetime
import functools
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from threading import Thread
from os import makedirs, getcwd
import os.path
import logging

from .ci_analyze import ci_analyze
from ..student import clone_student
from ..common import chdir, run
from ..specs import load_all_specs, check_dependencies, check_architecture
from .find_update import update_available
from .process_student import process_student
from .args import process_args, compute_stogit_url
from .progress_bar import progress_bar
from .save_recordings import save_recordings, gist_recordings
from .tabulate import tabulate
from ..webapp import server
from ..webapp.web_cli import launch_cli, check_web_spec


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


def run_server(basedir, port):
    server.exe_name = '"{}/server/server_file"'.format(basedir)
    server.run_server(port=port)
    return


def download_specs(course, basedir, stogit):
    spec_urls = {
        'sd': 'https://github.com/StoDevX/cs251-specs.git',
        'hd': 'https://github.com/StoDevX/cs241-specs.git',
        'ads': 'https://github.com/StoDevX/cs253-specs.git',
        'os': 'https://github.com/StoDevX/cs273-specs.git'
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


def run_analysis(*, no_progress=False, parallel, single_analysis, usernames, workers=1):
    results = []
    records = []

    if parallel:
        print_progress = make_progress_bar(usernames, no_progress=no_progress)
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(single_analysis, name) for name in usernames]
            for future in as_completed(futures):
                result, recording = future.result()
                print_progress(result['username'])
                results.append(result)
                records.extend(recording)
    else:
        for student in usernames:
            logging.debug('Processing {}'.format(student))
            result, recording = single_analysis(student)
            results.append(result)
            records.extend(recording)

    return results, records


def main():
    basedir = getcwd()
    args, usernames, assignments, stogit_url = process_args()
    ci = args['ci']
    clean = args['clean']
    course = args['course']
    date = args['date']
    debug = args['debug']
    gist = args['gist']
    highlight_partials = args['highlight_partials']
    interact = args['interact']
    no_check = args['no_check']
    no_update = args['no_update']
    no_progress = args['no_progress']
    port = args['server_port']
    quiet = args['quiet']
    skip_update_check = args['skip_update_check']
    skip_web_compile = args['skip_web_compile']
    sort_by = args['sort_by']
    stogit = args['stogit']
    web = args['web']
    workers = args['workers']

    if debug or interact:
        workers = 1

    current_version, new_version = update_available(skip_update_check=skip_update_check)
    if new_version:
        print(('v{} is available: you have v{}. '
               'Try "pip3 install --no-cache --user --upgrade stograde" '
               'to update.').format(new_version, current_version), file=sys.stderr)

    if date:
        logging.debug('Checking out {}'.format(date))

    if not os.path.exists("data"):
        if ci:
            if course:
                url = download_specs(course, basedir, stogit)
                if not stogit:
                    stogit_url = url
            else:
                print("data directory not found and no course specified")
                sys.exit(1)

        else:
            print('data directory not found', file=sys.stderr)
            if course:
                url = download_specs(course, basedir, stogit)
                if not stogit:
                    stogit_url = url
            else:
                download = input("Download specs? (Y/N)")
                if download and download.lower()[0] == "y":
                    repo = input("Which class? (SD/HD/ADS/OS)")
                    if repo:
                        url = download_specs(repo, basedir, stogit)
                        if not stogit:
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

        if ci:
            try:
                with open('.stogradeignore', encoding='utf-8') as infile:
                    ignored_specs = [line.strip() for line in infile.read().splitlines()]
                    logging.debug("Ignored specs: {}".format(ignored_specs))
                available_specs = available_specs.difference(ignored_specs)
            except FileNotFoundError:
                logging.debug("No .stogradeignore file found")

        for spec_to_use in assignments:
            try:
                check_dependencies(specs[spec_to_use])
                if not check_architecture(spec_to_use, specs[spec_to_use], ci):
                    available_specs.remove(spec_to_use)
            except KeyError:
                # Prevent lab0 directory from causing an extraneous output
                if spec_to_use != 'lab0':
                    print('Spec {} does not exist'.format(spec_to_use), file=sys.stderr)
                available_specs.remove(spec_to_use)

        assignments = available_specs

        if not assignments:
            print('No valid specs remaining', file=sys.stderr)
            sys.exit(1)
        else:
            logging.debug("Remaining specs: {}".format(assignments))

    results = []
    records = []
    if not ci:
        makedirs('./students', exist_ok=True)

    if ci or web:
        makedirs('./server', exist_ok=True)

    directory = './students' if not ci else '.'
    with chdir(directory):
        single_analysis = functools.partial(
            process_student,
            assignments=assignments,
            basedir=basedir,
            ci=ci,
            clean=clean,
            date=date,
            debug=debug,
            interact=interact,
            no_check=no_check,
            no_update=no_update,
            specs=specs,
            skip_web_compile=skip_web_compile,
            stogit_url=stogit_url
        )

        do_record = True

        if web:
            spec_id = list(assignments)[0]
            spec = specs[spec_id]
            web_spec = check_web_spec(spec)
            if not web_spec:
                print("No web files in assignment {}".format(list(assignments)[0]))
                sys.exit(1)

            Thread(target=run_server, args=(basedir, port,), daemon=True).start()

            for user in usernames:
                clone_student(user, baseurl=stogit_url)

            do_record = launch_cli(basedir=basedir,
                                   date=date,
                                   no_update=no_update,
                                   spec=spec,
                                   spec_id=spec_id,
                                   usernames=usernames)
            if not do_record:
                quiet = True

        if do_record:
            if workers > 1:
                results, records = run_analysis(no_progress=no_progress,
                                                parallel=True,
                                                single_analysis=single_analysis,
                                                usernames=usernames,
                                                workers=workers)
            else:
                results, records = run_analysis(no_progress=no_progress,
                                                parallel=False,
                                                single_analysis=single_analysis,
                                                usernames=usernames)

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
        passing = ci_analyze(records)
        if not passing:
            logging.debug('Build failed')
            sys.exit(1)
    else:
        save_recordings(records, debug=debug)
