from collections import defaultdict
from typing import List, TYPE_CHECKING, Callable, Mapping

from .group_type import GroupType
from ..common.group_by import group_by as group

if TYPE_CHECKING:
    from .formatted_result import FormattedResult
    from ..process_assignment.record_result import RecordResult
    from ..student.student_result import StudentResult


def format_collected_data(student_results: List['StudentResult'],
                          group_by: GroupType,
                          formatter: Callable[['RecordResult'],
                                              'FormattedResult']) -> Mapping[str, List['FormattedResult']]:
    """Turn the list of recordings into a list of nicely-formatted results.

    `grouped_records` will be a list of pairs: (assignment, recordings), where
    `assignment` is the assignment name and `recordings` is a list of recordings
    (one per student).

    `formatter` is a formatter. It receives each recording, one at a time, and should
    return a FormattedResult.
    """

    results = []
    for student in student_results:
        results.extend(student.results)

    if group_by is GroupType.ASSIGNMENT:
        grouped_records = group(results, predicate=lambda rec: rec.spec_id)
    elif group_by is GroupType.STUDENT:
        grouped_records = group(results, predicate=lambda rec: rec.student)
    else:
        raise TypeError('Invalid grouping type')

    student_results: Mapping[str, List['FormattedResult']] = defaultdict(list)

    for key, recordings in grouped_records:
        for content in recordings:
            student_results[key].append(formatter(content))

    return student_results
