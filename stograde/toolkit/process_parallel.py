from concurrent.futures import as_completed, ProcessPoolExecutor
import functools
import logging
from typing import List, Callable, Any

from ..toolkit.progress_bar import make_progress_bar


def process_parallel(students: List[str],
                     no_progress_bar: bool,
                     workers: int,
                     operation: functools.partial,
                     progress_indicator: Callable[[Any], str] = lambda value: value) -> List:
    results = []

    if workers > 1:
        print_progress = make_progress_bar(students, no_progress_bar=no_progress_bar)
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(operation, name) for name in students]
            for future in as_completed(futures):
                completed_student = future.result()
                print_progress(progress_indicator(completed_student))
                results.append(completed_student)
    else:
        for student in students:
            logging.debug('Processing {}'.format(student))
            completed_student = operation(student)
            results.append(completed_student)

    return results
