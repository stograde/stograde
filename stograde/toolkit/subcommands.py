import datetime
import functools
import logging
import os
import sys
from concurrent.futures._base import as_completed
from concurrent.futures.process import ProcessPoolExecutor
from os import makedirs
from threading import Thread
from typing import Dict, List, Any, TYPE_CHECKING

from . import global_vars
from .process_students import process_students
from .global_vars import DEBUG
from .progress_bar import make_progress_bar
from .save_recordings import save_recordings
from .stogit_url import compute_stogit_url
from .tabulate import tabulate
from ..common import chdir
from ..student.ci_analyze import ci_analyze
from ..student.process_student import prepare_student, prepare_student_repo
from ..webapp import server
from ..webapp.web_cli import is_web_spec, launch_cli

if TYPE_CHECKING:
    from ..specs.spec import Spec
    from ..student.student_result import StudentResult


def do_ci(specs: Dict[str, 'Spec'],
          students: List[str],
          base_dir: str,
          stogit_url: str,
          args: Dict[str, Any]):
    global_vars.CI = True
    skip_web_compile: bool = args['skip_web_compile']

    results: List['StudentResult'] = process_students(specs=specs,
                                                      students=students,
                                                      analyze=True,
                                                      base_dir=base_dir,
                                                      clean=False,
                                                      date='',
                                                      interact=False,
                                                      no_progress_bar=True,
                                                      record=True,
                                                      skip_branch_check=True,
                                                      skip_repo_update=True,
                                                      skip_web_compile=skip_web_compile,
                                                      stogit_url=stogit_url,
                                                      workers=1,
                                                      work_dir='./students')

    passing: bool = ci_analyze(results)
    if not passing:
        logging.debug('Build failed')
        sys.exit(1)


def do_record(specs: Dict[str, 'Spec'],
              students: List[str],
              base_dir: str,
              stogit_url: str,
              args: Dict[str, Any]):
    show_table: bool = args['table']

    clean: bool = args['clean']
    date: str = args['date']
    gist: bool = args['gist']
    interact: bool = args['interact']
    no_partials: bool = args['no_partials']
    no_progress_bar: bool = args['no_progress_bar']
    skip_branch_check: bool = args['skip_branch_check']
    skip_repo_update: bool = args['skip_repo_update']
    skip_web_compile: bool = args['skip_web_compile']
    sort_by: str = args['sort_by']
    workers: int = args['workers'] if not DEBUG and not interact else 1

    makedirs('./students', exist_ok=True)

    results: List['StudentResult'] = process_students(specs=specs,
                                                      students=students,
                                                      analyze=show_table,
                                                      base_dir=base_dir,
                                                      clean=clean,
                                                      date=date,
                                                      interact=interact,
                                                      no_progress_bar=no_progress_bar,
                                                      record=True,
                                                      skip_branch_check=skip_branch_check,
                                                      skip_repo_update=skip_repo_update,
                                                      skip_web_compile=skip_web_compile,
                                                      stogit_url=stogit_url,
                                                      workers=workers,
                                                      work_dir='./students')

    table: str = ''
    if show_table:
        table = tabulate(results, sort_by=sort_by, highlight_partials=not no_partials)
        print('\n' + table + '\n')

    save_recordings(results, table, gist=gist)


def do_table(specs: Dict[str, 'Spec'],
             students: List[str],
             base_dir: str,
             stogit_url: str,
             args: Dict[str, Any]):
    clean: bool = args['clean']
    date: str = args['date']
    no_partials: bool = args['no_partials']
    no_progress_bar: bool = args['no_progress_bar']
    skip_repo_update: bool = args['skip_repo_update']
    sort_by: str = args['sort_by']
    workers: int = args['workers'] if not DEBUG else 1

    results: List['StudentResult'] = process_students(specs=specs,
                                                      students=students,
                                                      analyze=True,
                                                      base_dir=base_dir,
                                                      clean=clean,
                                                      date=date,
                                                      interact=False,
                                                      no_progress_bar=no_progress_bar,
                                                      record=False,
                                                      skip_branch_check=True,
                                                      skip_repo_update=skip_repo_update,
                                                      skip_web_compile=True,
                                                      stogit_url=stogit_url,
                                                      workers=workers,
                                                      work_dir='./students')

    print('\n' + tabulate(results, sort_by=sort_by, highlight_partials=not no_partials) + '\n')


def do_web(specs: Dict[str, 'Spec'],
           students: List[str],
           base_dir: str,
           stogit_url: str,
           args: Dict[str, Any]):
    clean: bool = args['clean']
    date: str = args['date']
    skip_repo_update: bool = args['skip_repo_update']
    port: int = args['port']
    spec: 'Spec' = list(specs.values())[0]

    if not is_web_spec(spec):
        print("No web files in assignment {}".format(spec.id))
        sys.exit(1)

    Thread(target=server.run_server, args=(port,), daemon=True).start()

    launch_cli(base_dir=base_dir,
               clean=clean,
               date=date,
               skip_repo_update=skip_repo_update,
               spec=spec,
               stogit_url=stogit_url,
               students=students)


def do_clean(students: List[str],
             stogit_url: str,
             no_progress_bar: bool,
             workers: int):
    with chdir(os.path.join('.', 'students')):
        single_repo = functools.partial(
            prepare_student_repo,
            stogit_url=stogit_url,
            do_clean=True,
            do_clone=True,
            do_pull=True,
            do_checkout=False
        )

        process_parallel_repos(students=students,
                               no_progress_bar=no_progress_bar,
                               workers=workers,
                               operation=single_repo)


def do_update(students: List[str],
              stogit_url: str,
              no_progress_bar: bool,
              workers: int):
    with chdir(os.path.join('.', 'students')):
        single_repo = functools.partial(
            prepare_student_repo,
            stogit_url=stogit_url,
            do_clean=False,
            do_clone=True,
            do_pull=True,
            do_checkout=False
        )

        process_parallel_repos(students=students,
                               no_progress_bar=no_progress_bar,
                               workers=workers,
                               operation=single_repo)


def process_parallel_repos(students: List[str],
                           no_progress_bar: bool,
                           workers: int,
                           operation: functools.partial):
    if workers > 1:
        print_progress = make_progress_bar(students, no_progress_bar=no_progress_bar)
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(operation, name) for name in students]
            for future in as_completed(futures):
                completed_student = future.result()
                print_progress(completed_student)
    else:
        for student in students:
            logging.debug('Processing {}'.format(student))
            operation(student)
