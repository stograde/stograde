import functools
from typing import List

from .process_parallel import process_parallel
from ..common import chdir
from ..specs.spec import Spec
from ..student.process_student import process_student
from ..student.student_result import StudentResult


def process_students(specs: List['Spec'],
                     students: List[str],
                     *,
                     analyze: bool,
                     base_dir: str,
                     clean: bool,
                     date: str,
                     interact: bool,
                     no_progress_bar: bool,
                     record: bool,
                     skip_branch_check: bool,
                     skip_repo_update: bool,
                     skip_web_compile: bool,
                     stogit_url: str,
                     workers: int,
                     work_dir: str) -> List['StudentResult']:
    with chdir(work_dir):
        single_analysis = functools.partial(
            process_student,
            analyze=analyze,
            basedir=base_dir,
            clean=clean,
            date=date,
            interact=interact,
            skip_branch_check=skip_branch_check,
            skip_repo_update=skip_repo_update,
            record=record,
            specs=specs,
            skip_web_compile=skip_web_compile,
            stogit_url=stogit_url
        )

        results: List['StudentResult'] = process_parallel(students,
                                                          no_progress_bar,
                                                          workers,
                                                          single_analysis,
                                                          progress_indicator=lambda value: value.name)

    return results
