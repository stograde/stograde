import os
from logging import warning

from cs251tk.formatters import format_collected_data, markdown, gist
from .gist import post_gist
from .tabulate import asciiify


def record_recording_to_disk(results, file_identifier):
    results = sorted(results, key=lambda file: file['student'])
    results = [file['content'] for file in results]
    output = '\n'.join(results)
    try:
        os.makedirs('logs', exist_ok=True)
        with open('logs/log-{}.md'.format(file_identifier), 'w', encoding='utf-8') as outfile:
            outfile.write(output)
    except Exception as err:
        warning('error! could not write recording:', err)


def send_recording_to_gist(table, results, assignment):
    """Publish a table/result pair to a private gist"""

    # the "-" at the front is so that github sees it first and names the gist
    # after the homework
    table_filename = '-cs251 report %s table.txt' % assignment
    files = {
        table_filename: {'content': table},
    }

    for file in results:
        filename = file['student'] + '.' + file['type']
        files[filename] = {
            'content': file['content'].strip()
        }

    return post_gist('log for ' + assignment, files)


def save_recordings(records, debug=False):
    """Take the list of recordings, group by assignment, then save to disk"""

    results = format_collected_data(records,
                                    group_by='assignment',
                                    formatter=markdown,
                                    debug=debug)

    for assignment, content in results.items():
        record_recording_to_disk(content, assignment)


def gist_recordings(records, table, debug=False):
    """Take the list of recordings, group by assignment, then post to a private gist"""

    results = format_collected_data(records,
                                    group_by='assignment',
                                    formatter=gist,
                                    debug=debug)

    for assignment, content in results.items():
        # clean up the table and make it plain ascii
        table = asciiify(table)
        url = send_recording_to_gist(table, content, assignment)
        print(assignment, 'results are available at', url)
