from concurrent.futures import ProcessPoolExecutor, as_completed
import datetime
import functools
import logging
from os import getcwd, makedirs
import os.path
import sys
from threading import Thread
from typing import List

from .args import process_args
from .ci_analyze import ci_analyze
from .download_specs import create_data_dir
from .find_update import update_available
from .process_student import process_student
from .progress_bar import progress_bar
from .save_recordings import save_recordings
from .stogit_url import compute_stogit_url
from .tabulate import tabulate
from ..common import chdir
from ..specs import check_architecture, check_dependencies, delete_cache, load_all_specs
from ..specs.spec import Spec
from ..student import clone_student
from ..student.student_result import StudentResult
from ..webapp import server
from ..webapp.web_cli import check_web_spec, launch_cli


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


def run_server(port):
    server.run_server(port=port)
    return


def run_analysis(*,
                 no_progress: bool = False,
                 parallel: bool,
                 single_analysis: functools.partial,
                 usernames: List[str],
                 workers: int = 1) -> List[StudentResult]:
    results: List[StudentResult] = []

    if parallel:
        print_progress = make_progress_bar(usernames, no_progress=no_progress)
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(single_analysis, name) for name in usernames]
            for future in as_completed(futures):
                result: StudentResult = future.result()
                print_progress(result.name)
                results.append(result)
    else:
        for student in usernames:
            logging.debug('Processing {}'.format(student))
            result: StudentResult = single_analysis(student)
            results.append(result)

    return results


def main():
    basedir = getcwd()
    args, usernames, assignments = process_args()
    ci = args['ci']
    clean = args['clean']
    course = args['course']
    date = args['date']
    debug = args['debug']
    gist = args['gist']
    highlight_partials = args['highlight_partials']
    interact = args['interact']
    no_branch_check = args['no_check']
    no_update = args['no_update']
    no_progress = args['no_progress']
    port = args['server_port']
    re_cache_specs = args['re_cache']
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
        create_data_dir(ci, course, basedir)

    stogit_url = compute_stogit_url(stogit=stogit, course=course, _now=datetime.date.today())

    if re_cache_specs:
        delete_cache(basedir)

    specs: List[Spec] = load_all_specs(basedir=os.path.join(basedir, 'data'), skip_update_check=skip_update_check)
    loaded_specs = {spec.id: spec for spec in specs}

    if not specs:
        print('No specs loaded!')
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

        for spec_id in assignments:
            spec_to_use = loaded_specs[spec_id]
            try:
                check_dependencies(spec_to_use)
                if not check_architecture(spec_to_use, ci):
                    available_specs.remove(spec_to_use.id)
            except KeyError:
                # Prevent lab0 directory from causing an extraneous output
                if spec_to_use.id != 'lab0':
                    print('Spec {} does not exist'.format(spec_to_use.id), file=sys.stderr)
                available_specs.remove(spec_to_use.id)

        assignments = available_specs

        if not assignments:
            print('No valid specs remaining', file=sys.stderr)
            sys.exit(1)
        else:
            logging.debug("Remaining specs: {}".format(assignments))

    results = []
    if not ci:
        makedirs('./students', exist_ok=True)

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
            no_branch_check=no_branch_check,
            no_repo_update=no_update,
            specs=specs,
            skip_web_compile=skip_web_compile,
            stogit_url=stogit_url
        )

        do_record = True

        if web:
            spec_id = list(assignments)[0]
            spec = loaded_specs[spec_id]
            web_spec = check_web_spec(spec)
            if not web_spec:
                print("No web files in assignment {}".format(spec_id))
                sys.exit(1)

            Thread(target=run_server, args=(port,), daemon=True).start()

            for user in usernames:
                clone_student(user, base_url=stogit_url)

            do_record = launch_cli(basedir=basedir,
                                   date=date,
                                   no_repo_update=no_update,
                                   spec=spec,
                                   usernames=usernames)
            if not do_record:
                quiet = True

        if do_record:
            if workers > 1:
                results: List[StudentResult] = run_analysis(no_progress=no_progress,
                                                            parallel=True,
                                                            single_analysis=single_analysis,
                                                            usernames=usernames,
                                                            workers=workers)
            else:
                results: List[StudentResult] = run_analysis(no_progress=no_progress,
                                                            parallel=False,
                                                            single_analysis=single_analysis,
                                                            usernames=usernames)

    table = ''
    if ci or gist or not quiet:
        table: str = tabulate(results, sort_by=sort_by, highlight_partials=highlight_partials)

    if ci or not quiet:
        print('\n' + table + '\n')

    save_recordings(results, table, debug=debug, gist=gist)

    if ci:
        passing: bool = ci_analyze(results)
        if not passing:
            logging.debug('Build failed')
            sys.exit(1)
