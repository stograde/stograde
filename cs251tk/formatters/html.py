from textwrap import indent
import traceback
import html


def format_assignment_html(recording, debug=False):
    """Given a single recording, format it into an HTML file.

    Each recording will only have one student.

    Returns a {content: str, student: str, type: str, assignment: str} dict.
    """

    try:
        files = format_files_list(recording.get('files', {}))
        warnings = format_warnings(recording.get('warnings', {}).items())
        header = format_header(recording, warnings)
        output = (header + files) + '\n\n'

    except Exception as err:
        if debug:
            raise err
        output = format_as_code(traceback.format_exc())

    return {
        'assignment': recording['spec'],
        'content': output,
        'student': recording['student'],
        'type': 'html',
    }


def format_files_list(files):
    return '\n\n'.join([format_file(name, info) for name, info in files.items()])


def format_warnings(warnings):
    formatted = [format_warning(warning, value) for warning, value in warnings]
    return [w for w in formatted if w]


def format_header(recording, warnings):
    header = '<h1>{spec}</h1>'.format_map(recording)

    if warnings:
        header += format_as_ul(''.join(warnings))

    return header


def format_warning(w, value):
    if w == 'no submission':
        return '<li>No submission found.</li>'

    elif w == 'unmerged branches' and value:
        branches = ['<li>{}</li>'.format(b) for b in value]
        return '<li>Repository has unmerged branches:<ul>{}</ul></li>'.format('\n'.join(branches))

    elif value:
        return '<li>Warning: {}</li>'.format(value)

    else:
        return ''


def format_file(filename, file_info):
    contents = format_file_contents(file_info.get('contents', ''), file_info) + '\n'
    compilation = format_file_compilation(file_info.get('compilation', [])) + '\n'
    test_results = format_file_results(file_info.get('result', [])) + '\n'

    if file_info.get('last modified', None):
        last_modified = ' (last modified on {})'.format(file_info['last modified'])
    else:
        last_modified = ''

    file_header = '<h2><code>{}</code>{}</h2>'.format(filename, last_modified)

    if file_info['missing']:
        note = '<code>{}</code> was not found. We found these files:\n'.format(filename)
        directory_listing = format_as_ul(['<li><code>{}</code></li>'.format(f) for f in file_info.get('other files', [])])

        if file_info['optional']:
            file_header = file_header.strip()
            file_header += ' (<strong>optional submission</strong>)\n'

        return '\n'.join([file_header, note, directory_listing + '\n\n'])

    return '\n'.join([file_header, contents, compilation, test_results])


def format_file_contents(contents, info):
    return format_as_code(html.escape(contents))


def format_file_compilation(compilations):
    result = []
    for status in compilations:
        output = status['output']
        command = '<code>{command}</code>'.format_map(status)

        if not output:
            result.append('<p><strong>no warnings: {}</strong></p>'.format(command))
        else:
            result.append('<p><strong>warnings: {}</strong></p>'.format(command))
            result.append(format_as_code(output))

    return '\n'.join(result)


def format_file_results(test_results):
    result = ''

    for test in test_results:
        header = '<p><strong>results of <code>{command}</code></strong> (status: {status})</p>'.format_map(test)
        output = format_as_code(test['output'])
        result += header + '\n' + output

        if test['truncated']:
            result += '<p><em>(truncated after {truncated after})</em></p>'.format_map(test)

    return result


def format_as_code(data):
    if not data:
        return ''
    return '<pre><code>{}</code></pre>'.format(data)


def format_as_ul(data):
    if not data:
        return ''
    return '<ul>{}</ul>'.format(''.join(data))
