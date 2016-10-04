from textwrap import indent
from .markdown import format_warnings, format_header, format_file_compilation, format_file_results
import traceback


def format_assignment_gist(recording, debug=False):
    """Given a single recording, format it into a markdown file.

    Each recording will only have one student.

    Returns a {content: str, student: str, type: str} dict.
    """

    try:
        files = format_files_list(recording.get('files', {}))
        warnings = format_warnings(recording.get('warnings', {}).items())
        header = format_header(recording, warnings)
        output = (header + files) + '\n\n'

    except Exception as err:
        if debug:
            raise err
        output = indent(traceback.format_exc(), ' ' * 4) + '\n\n'

    return {
        'content': output,
        'student': recording['student'],
        'type': 'md',
    }


def format_files_list(files):
    return '\n\n' + '\n\n'.join([format_file(name, info) for name, info in files.items()])


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
        directory_listing = indent('\n'.join(file_info.get('other files', [])), ' ' * 4)

        if file_info['optional']:
            file_header = file_header.strip()
            file_header += ' (**optional submission**)\n'

        return '\n'.join([file_header, note, directory_listing + '\n\n'])

    return '\n'.join([file_header, contents, compilation, test_results])


def format_file_contents(contents, info):
    if not contents:
        return ''
    return '```{}\n{}\n```'.format(
        identify_type(info['filename']),
        contents)


def identify_type(filename):
    ext = filename.split('.')[-1]
    if ext == filename or ext == 'txt':
        return 'text'
    elif ext in ['C', 'H', 'cpp', 'hpp', 'h']:
        return 'cpp'
    elif ext in ['c']:
        return 'c'
    return ext
