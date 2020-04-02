from concurrent.futures import ProcessPoolExecutor, as_completed
import datetime
import functools
import logging
from os import getcwd, makedirs
import os.path
import sys
from threading import Thread
from typing import List, Dict

from .args import process_args
from stograde.student.ci_analyze import ci_analyze
from .download_specs import create_data_dir
from .filter_specs import filter_assignments, filter_specs
from .find_update import update_available
from stograde.student.process_student import process_student
from .progress_bar import progress_bar
from .save_recordings import save_recordings
from .stogit_url import compute_stogit_url
from .tabulate import tabulate
from ..common import chdir
from ..specs import delete_cache, load_all_specs
from ..specs.load import load_specs
from ..specs.spec import Spec
from ..student import clone_student
from ..student.student_result import StudentResult
from ..webapp import server
from ..webapp.web_cli import is_web_spec, launch_cli


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
    ci: bool = args['ci']
    clean: bool = args['clean']
    course: str = args['course']
    date = args['date']
    debug: bool = args['debug']
    gist = args['gist']
    highlight_partials: bool = args['highlight_partials']
    interact: bool = args['interact']
    no_branch_check: bool = args['no_check']
    no_update: bool = args['no_update']
    no_progress: bool = args['no_progress']
    port: int = args['server_port']
    re_cache_specs: bool = args['re_cache']
    quiet: bool = args['quiet']
    skip_update_check: bool = args['skip_update_check']
    skip_web_compile: bool = args['skip_web_compile']
    sort_by: str = args['sort_by']
    stogit: str = args['stogit']
    web: bool = args['web']
    workers: int = args['workers']

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

    assignments = filter_assignments(assignments, ci)

    if ci or quiet:
        # load specified specs
        loaded_specs: Dict[str, Spec] = load_specs(assignments,
                                                   data_dir=os.path.join(basedir, 'data'),
                                                   skip_update_check=skip_update_check)
    else:
        # load all
        loaded_specs: Dict[str, Spec] = load_all_specs(data_dir=os.path.join(basedir, 'data'),
                                                       skip_update_check=skip_update_check)

    if not loaded_specs:
        print('No specs loaded!')
        sys.exit(1)

    if assignments:
        assignments = filter_specs(assignments, loaded_specs, ci)

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
            specs=loaded_specs,
            skip_web_compile=skip_web_compile,
            stogit_url=stogit_url
        )

        do_record = True

        if web:
            spec_id = list(assignments)[0]
            spec = loaded_specs[spec_id]

            if not is_web_spec(spec):
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
            results: List[StudentResult] = run_analysis(no_progress=no_progress,
                                                        parallel=workers > 1,
                                                        single_analysis=single_analysis,
                                                        usernames=usernames,
                                                        workers=workers)

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
