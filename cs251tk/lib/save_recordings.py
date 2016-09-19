from .format_collected_data import format_collected_data
from .helpers import warn, flatten, group_by
import yaml
from .columnize import asciiify
from .gist import post_gist
import os


def record_recording_to_disk(results, file_identifier):
    results = sorted(results, key=lambda file: file['student'])
    results = [file['content'] for file in results]
    output = '\n'.join(results)
    try:
        os.makedirs('logs', exist_ok=True)
        with open('logs/log-{}.md'.format(file_identifier), 'w', encoding='utf-8') as outfile:
            outfile.write(output)
    except Exception as err:
        warn('error! could not write recording:', err)


def send_recording_to_gist(table, results, assignment):
    # the - at the front is so that github sees it first and names the gist
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


def save_recordings(records, table, destination='file', debug=False):
    # clean up the table and make it plain ascii
    table = asciiify(table)

    results = {}
    records = list(flatten(records))
    grouped_records = group_by(records, lambda rec: rec.get('spec', None))

    for assignment, recordings in grouped_records:
        for content in recordings:
            if debug:
                formatted = '---\n' + yaml.safe_dump(content, default_flow_style=False)
            else:
                formatted = format_collected_data(content, destination == 'gist')

            if assignment not in results:
                results[assignment] = []
            results[assignment].append({
                'content': formatted,
                'student': content['student'],
                'type': 'yaml' if debug else 'md',
            })

    for assignment, content in results.items():
        if destination == 'file':
            record_recording_to_disk(content, assignment)
        elif destination == 'gist':
            url = send_recording_to_gist(table, content, assignment)
            print(assignment, 'results are available at', url)
