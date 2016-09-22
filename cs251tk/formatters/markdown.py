from textwrap import indent
import traceback
from collections import defaultdict
from cs251tk.common import group_by as group


def format_collected_data(records, group_by: str, debug):
    """Turn the list of recordings into a list of nicely-formatted results.

    `grouped_records` will be a list of pairs: (assignment, recordings), where
    `assignment` is the assignment name and `recordings` is a list of recordings
    (one per student).
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
            results[key].append(format_assignment(content, debug=debug))

    return results


def format_assignment(recording, debug=False):
    """Given a single recording, format it into a markdown file.

    Each recording will only have one student.
    """

    try:
        files = format_files_list(recording.get('files', {}))
        warnings = [format_warning(warning, value) for warning, value in recording['warnings'].items()]
        warnings = [w for w in warnings if w]

        header = '# {spec} – {student}\n'.format_map(recording)

        if warnings:
            header += '\n' + '\n'.join(warnings) + '\n'

        if files:
            files = '\n\n' + files

        output = (header + files) + '\n\n'

    except Exception as err:
        if debug:
            raise err
        output = indent(traceback.format_exc(), ' '*4) + '\n\n'

    return {
        'content': output,
        'student': recording['student'],
        'type': 'md',
    }


def format_files_list(files):
    return '\n\n'.join([format_file(*f) for f in files.items()])


def format_warning(w, value):
    if w == 'no submission':
        return 'No submission found.\n'

    elif w == 'unmerged branches' and value:
        branches = ['  - ' + b for b in value]
        return 'Repository has unmerged branches:\n{}'.format('\n'.join(branches))

    elif value:
        return 'Warning: ' + value

    else:
        return ''


def format_file(filename, file_info):
    contents = format_file_contents(file_info.get('contents', ''), file_info) + '\n'
    compilation = format_file_compilation(file_info.get('compilation', [])) + '\n'
    test_results = format_file_results(file_info.get('result', [])) + '\n'

    if file_info.get('last modified', None):
        last_modified = ' ({})'.format(file_info['last modified'])
    else:
        last_modified = ''

    file_header = '## {}{}\n'.format(filename, last_modified)

    if file_info['missing']:
        note = 'File not found. `ls .` says that these files exist:\n'
        directory_listing = indent('\n'.join(file_info.get('other files', [])), ' '*4)

        if file_info['optional']:
            file_header = file_header.strip()
            file_header += ' (**optional submission**)\n'

        return '\n'.join([file_header, note, directory_listing + '\n\n'])

    return '\n'.join([file_header, contents, compilation, test_results])


def format_file_contents(contents, info):
    if not contents:
        return ''
    return indent(contents, '    ')


def format_file_compilation(compilations):
    result = []
    for status in compilations:
        output = status['output']
        command = '`{command}`'.format_map(status)

        if not output:
            result.append('**no warnings: {}**\n'.format(command))
        else:
            result.append('**warnings: {}**\n'.format(command))
            result.append(indent(output, ' '*4))

    return '\n'.join(result)


def format_file_results(test_results):
    result = ''

    for test in test_results:
        header = '**results of `{command}`** (status: {status})\n'.format_map(test)
        output = indent(test['output'], '    ')
        result += header + '\n' + output
        if test['truncated']:
            result += '\n' + '(truncated after {truncated after})'.format_map(test)

    return result


def em(string):
    return '**' + string + '**'


def code(string):
    return '`' + string + '`'
