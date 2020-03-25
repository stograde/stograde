from collections import defaultdict
from typing import List

from ..common import group_by as group
from ..student.student_result import StudentResult


def format_collected_data(student_results: List[StudentResult],
                          group_by: str,
                          formatter,
                          debug: bool) -> defaultdict:
    """Turn the list of recordings into a list of nicely-formatted results.

    `grouped_records` will be a list of pairs: (assignment, recordings), where
    `assignment` is the assignment name and `recordings` is a list of recordings
    (one per student).

    `formatter` is a formatter. It receives each recording, one at a time, and should
    return a {content: str, student: str, type: str, assignment: str} dict for each
    recording.
    """

    results = []
    for student in student_results:
        results.extend(student.results)

    if group_by == 'assignment':
        grouped_records = group.group_by(results, lambda rec: rec.spec_id)
    elif group_by == 'student':
        grouped_records = group.group_by(results, lambda rec: rec.student)
    else:
        # not entirely sure what this'll do
        grouped_records = results

    student_results = defaultdict(list)
    for key, recordings in grouped_records:
        for content in recordings:
            student_results[key].append(formatter(content, debug=debug))

    return student_results
