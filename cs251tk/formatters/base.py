from collections import defaultdict
from cs251tk.common import group_by as group


def format_collected_data(records, group_by: str, formatter, debug):
    """Turn the list of recordings into a list of nicely-formatted results.

    `grouped_records` will be a list of pairs: (assignment, recordings), where
    `assignment` is the assignment name and `recordings` is a list of recordings
    (one per student).

    `formatter` is a formatter. It receives each recording, one at a time, and should
    return a {content: str, student: str, type: str, assignment: str} dict for each
    recording.
    """

    if group_by == 'assignment':
        grouped_records = group(records, lambda rec: rec.get('spec', None))
    elif group_by == 'student':
        grouped_records = group(records, lambda rec: rec.get('student', None))
    else:
        # not entirely sure what this'll do
        grouped_records = records

    results = defaultdict(list)
    for key, recordings in grouped_records:
        for content in recordings:
            results[key].append(formatter(content, debug=debug))

    return results
