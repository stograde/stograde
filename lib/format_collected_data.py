from textwrap import dedent, indent


def em(string):
    return '**' + string + '**'


def code(string):
    return '`' + string + '`'


def format_file_contents(contents):
    if not contents:
        return ''
    return indent(contents, '    ')


def format_file_compilation(compilations):
    result = []
    for status in compilations:
        output = status['output']
        command = '`{}`'.format(status['command'])
        if not output:
            result.append('**no warnings: {}**\n'.format(command))
        else:
            result.append('**warnings: {}**\n'.format(command))
            result.append(output)
    return '\n'.join(result)


def format_file_results(test_results):
    result = ''
    for test in test_results:
        header = '**results of `{}`** (status: {})\n'.format(test['command'], test['status'])
        output = indent(test['output'], '    ')
        result += header + '\n' + output
        if test['truncated']:
            result += '\n' + '(truncated after {})'.format(test['truncated after'])
    return result


def format_file(filename, file_info):
    contents = format_file_contents(file_info.get('contents', '')) + '\n'
    compilation = format_file_compilation(file_info.get('compilation', [])) + '\n'
    test_results = format_file_results(file_info.get('result', [])) + '\n'

    file_header = '## {} ({})'.format(filename, file_info['last modified']) + '\n'

    if file_info['missing']:
        return '\n'.join([file_header, directory_listing])
    return '\n'.join([file_header, contents, compilation, test_results])


def format_files(files):
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


def format_student(data):
    warnings = [format_warning(warning, value) for warning, value in data['warnings'].items()]
    warnings = [w for w in warnings if w]
    files = format_files(data.get('files', {}))

    header = '# {} – {}\n'.format(data['spec'], data['student'])

    if warnings:
        header += '\n' + '\n'.join(warnings) + '\n'

    if files:
        files = '\n\n' + files

    return dedent(header + files)


def format_collected_data(data):
    try:
        formatted_chunks = format_student(data)
    except Exception as e:
        formatted_chunks = repr(e)
    return formatted_chunks + '\n\n'
