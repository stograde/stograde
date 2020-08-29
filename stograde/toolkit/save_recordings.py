import logging
import os
import sys
from typing import List, TYPE_CHECKING, Mapping

from .gist import post_gist
from ..formatters import format_collected_data, markdown, html
from ..formatters.format_type import FormatType
from ..formatters.group_type import GroupType
from ..formatters.html_template import add_styling
from ..formatters.tabulate import asciiify

if TYPE_CHECKING:
    from ..formatters.formatted_result import FormattedResult
    from ..student.student_result import StudentResult


def record_recording_to_disk(results: List['FormattedResult'], file_identifier: str, format_type: FormatType):
    results = sorted(results, key=lambda file: file.student)
    students = [res.student for res in results]
    results = [file.content for file in results]
    output = '\n'.join(results)
    if format_type is FormatType.HTML:
        output = add_styling(file_identifier, students, output)
    try:
        os.makedirs('logs', exist_ok=True)
        with open('logs/log-{}.{}'.format(file_identifier, format_type.name.lower()), 'w', encoding='utf-8') as outfile:
            outfile.write(output)
    except Exception as err:
        print('Could not write recording for {}: {}'.format(file_identifier, str(err)), file=sys.stderr)


def send_recording_to_gist(table: str, results: List['FormattedResult'], assignment: str):
    """Publish a table/result pair to a private gist"""

    # the "-" at the front is so that github sees it first and names the gist
    # after the homework
    table_filename = '-stograde report {} table.txt'.format(assignment)
    files = {
        table_filename: {'content': table},
    }

    for file in results:
        filename = file.student + '.' + file.type.name.lower()
        files[filename] = {
            'content': file.content.strip()
        }

    return post_gist('log for ' + assignment, files)


def save_recordings(results: List['StudentResult'],
                    table: str,
                    gist: bool = False,
                    format_type: 'FormatType' = FormatType.MD):
    """Take the list of recordings, group by assignment, then save to disk"""

    if format_type is FormatType.MD:
        formatter = markdown
    elif format_type is FormatType.HTML:
        formatter = html
    else:
        formatter = markdown

    formatted_results: Mapping[str, List['FormattedResult']] = format_collected_data(results,
                                                                                     group_by=GroupType.ASSIGNMENT,
                                                                                     formatter=formatter)

    for assignment, content in formatted_results.items():
        logging.debug("Saving recording for {}".format(assignment))
        if gist:
            table = asciiify(table)
            url = send_recording_to_gist(table, content, assignment)
            print('{} results are available at {}'.format(assignment, url))
        else:
            record_recording_to_disk(content, assignment, format_type)
