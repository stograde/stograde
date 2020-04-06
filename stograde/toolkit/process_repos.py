from concurrent.futures import as_completed, ProcessPoolExecutor
import functools
import logging
from typing import List

from ..toolkit.progress_bar import make_progress_bar


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
