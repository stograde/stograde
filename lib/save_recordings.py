from .format_collected_data import format_collected_data
from .helpers import warn, flatten, group_by


def record_recording_to_disk(results, file_identifier):
    output = '\n'.join([r['content'] for r in results])
    try:
        with open('logs/log-{}.md'.format(file_identifier), 'w', encoding='utf-8') as outfile:
            outfile.write(output)
    except Exception as err:
        warn('error! could not write recording:', err)


def save_recordings(records, table, debug=False):
    # clean up the table and make it plain ascii
    table = asciiify(table)

    results = {}
    records = list(flatten(records))
    grouped_records = group_by(records, lambda rec: rec.get('spec', None))

    for assignment, recordings in grouped_records:
        for content in recordings:
            if debug:
                formatted = '---\n' + yaml.dump(content)
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
        record_recording_to_disk(content, assignment)
