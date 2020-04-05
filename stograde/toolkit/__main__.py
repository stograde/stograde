import datetime
import logging
import os.path
import sys
from os import getcwd, makedirs
from threading import Thread
from typing import List, Dict, TYPE_CHECKING, Any

from .args import process_args, DEBUG
from .download_specs import create_data_dir
from .filter_specs import filter_assignments, filter_specs
from .find_update import update_available
from .process_students import process_students
from .save_recordings import save_recordings
from .stogit_url import compute_stogit_url
from .tabulate import tabulate
from ..specs import load_specs
from ..student.ci_analyze import ci_analyze
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
    skip_web_compile: bool = args['skip_web_compile']

    results: List['StudentResult'] = process_students(specs=specs,
                                                      students=students,
                                                      analyze=True,
                                                      base_dir=base_dir,
                                                      clean=False,
                                                      date='',
                                                      interact=False,
                                                      no_branch_check=True,
                                                      no_progress_bar=True,
                                                      no_repo_update=True,
                                                      record=True,
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
    no_branch_check: bool = args['no_branch_check']
    no_progress_bar: bool = args['no_progress_bar']
    no_repo_update: bool = args['no_repo_update']
    partials: bool = args['partials']
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
                                                      no_branch_check=no_branch_check,
                                                      no_progress_bar=no_progress_bar,
                                                      no_repo_update=no_repo_update,
                                                      record=True,
                                                      skip_web_compile=skip_web_compile,
                                                      stogit_url=stogit_url,
                                                      workers=workers,
                                                      work_dir='./students')

    table: str = ''
    if show_table:
        table = tabulate(results, sort_by=sort_by, highlight_partials=partials)
        print('\n' + table + '\n')

    save_recordings(results, table, gist=gist)


def do_table(specs: Dict[str, 'Spec'],
             students: List[str],
             base_dir: str,
             stogit_url: str,
             args: Dict[str, Any]):
    clean: bool = args['clean']
    date: str = args['date']
    interact: bool = args['interact']
    no_branch_check: bool = args['no_branch_check']
    no_progress_bar: bool = args['no_progress_bar']
    no_repo_update: bool = args['no_repo_update']
    partials: bool = args['partials']
    skip_web_compile: bool = args['skip_web_compile']
    sort_by: str = args['sort_by']
    workers: int = args['workers'] if not DEBUG and not interact else 1

    results: List['StudentResult'] = process_students(specs=specs,
                                                      students=students,
                                                      analyze=True,
                                                      base_dir=base_dir,
                                                      clean=clean,
                                                      date=date,
                                                      interact=interact,
                                                      no_branch_check=no_branch_check,
                                                      no_progress_bar=no_progress_bar,
                                                      no_repo_update=no_repo_update,
                                                      record=False,
                                                      skip_web_compile=skip_web_compile,
                                                      stogit_url=stogit_url,
                                                      workers=workers,
                                                      work_dir='./students')

    print('\n' + tabulate(results, sort_by=sort_by, highlight_partials=partials) + '\n')


def do_web(specs: Dict[str, 'Spec'],
           students: List[str],
           base_dir: str,
           stogit_url: str,
           args: Dict[str, Any]):
    clean: bool = args['clean']
    date: str = args['date']
    no_repo_update: bool = args['no_repo_update']
    port: int = args['port']
    spec: 'Spec' = list(specs.values())[0]

    if not is_web_spec(spec):
        print("No web files in assignment {}".format(spec.id))
        sys.exit(1)

    Thread(target=server.run_server, args=(port,), daemon=True).start()

    launch_cli(base_dir=base_dir,
               clean=clean,
               date=date,
               no_repo_update=no_repo_update,
               spec=spec,
               stogit_url=stogit_url,
               students=students)


def main():
    basedir = getcwd()
    args, usernames, assignments = process_args()
    course: str = args['course']
    date: str = args['date']
    skip_update_check: bool = args['skip_update_check']
    stogit: str = args['stogit']

    current_version, new_version = update_available(skip_update_check=skip_update_check)
    if new_version:
        print(('v{} is available: you have v{}. '
               'Try "pip3 install --no-cache --user --upgrade stograde" '
               'to update.').format(new_version, current_version), file=sys.stderr)

    if date:
        logging.debug('Checking out {}'.format(date))

    if not os.path.exists("data"):
        create_data_dir(course, basedir)

    stogit_url = compute_stogit_url(stogit=stogit, course=course, _now=datetime.date.today())

    assignments = filter_assignments(assignments)

    loaded_specs: Dict[str, 'Spec'] = load_specs(assignments,
                                                 data_dir=os.path.join(basedir, 'data'),
                                                 skip_update_check=skip_update_check)

    if not loaded_specs:
        print('No specs loaded!')
        sys.exit(1)

    if assignments:
        assignments = filter_specs(assignments, loaded_specs)

        if not assignments:
            print('No valid specs remaining', file=sys.stderr)
            sys.exit(1)
        else:
            logging.debug("Remaining specs: {}".format(assignments))
