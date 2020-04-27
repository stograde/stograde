import functools
import logging
from concurrent.futures import as_completed, ProcessPoolExecutor
from typing import List

from ..common import chdir
from ..specs.spec import Spec
from ..student.process_student import process_student
from ..student.student_result import StudentResult
from ..toolkit.progress_bar import make_progress_bar


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

        results: List['StudentResult'] = []

        if workers > 1:
            print_progress = make_progress_bar(students, no_progress_bar=no_progress_bar)
            with ProcessPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(single_analysis, name) for name in students]
                for future in as_completed(futures):
                    result: 'StudentResult' = future.result()
                    print_progress(result.name)
                    results.append(result)
        else:
            for student in students:
                logging.debug('Processing {}'.format(student))
                result: 'StudentResult' = single_analysis(student)
                results.append(result)

    return results
