import os
import shlex
from glob import glob
from collections import OrderedDict
from os.path import exists, join as path_join
from .find_unmerged_branches_in_cwd import find_unmerged_branches_in_cwd
from .run import run
from .helpers import flatten


def unicode_truncate(string, length, encoding='utf-8'):
    encoded = string.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')


def expand_chunk(command_chunk):
    '''Take a chunk of a command and expand it, like a shell'''
    # TODO: Support escaped globs
    if '*' in command_chunk:
        return glob(command_chunk)
    return command_chunk


def process_chunk(command):
    '''Takes one piece of a pipeline and formats it for run_command'''
    # decode('unicode_escape') de-escapes the backslash-escaped strings.
    # like, it turns the \n from "echo Hawken \n 26" into an actual newline,
    # like a shell would.
    cmd = bytes(command, 'utf-8').decode('unicode_escape')

    # shlex splits commands up like a shell does.
    # I'm not entirely sure how it differs from just split(' '),
    # but figured it wasn't a bad thing to use.
    cmds = shlex.split(cmd)

    cmds = list(flatten([expand_chunk(c) for c in cmds]))

    return cmds


def kinda_pipe_commands(cmd_string):
    cmds = cmd_string.split(' | ')

    input_for_cmd = None
    for cmd in cmds[:-1]:
        cmd = process_chunk(cmd)
        _, input_for_cmd = run(cmd, input=input_for_cmd)
        input_for_cmd = input_for_cmd.encode('utf-8')

    final_cmd = process_chunk(cmds[-1])
    return (final_cmd, input_for_cmd)


def process_file(filename, steps, options, spec, cwd, supporting_dir):
    steps = steps if isinstance(steps, list) else [steps]

    options = {
        'timeout': 4,
        'truncate_output': 10000,  # 10K
        'truncate_contents': False,
        'optional': False,
        'hide_contents': False,
    }
    options.update(options)

    results = {
        'filename': filename,
        'missing': False,
        'compilation': [],
        'result': [],
    }

    file_status, file_contents = run(['cat', filename])
    if file_status == 'success':
        _, last_edit = run(['git', 'log',
                            '-n', '1',
                            '--pretty=format:%cd',
                            '--', filename])
        results['last modified'] = last_edit

    if options['hide_contents']:
        file_contents = ''
    elif options['truncate_contents']:
        file_contents = unicode_truncate(file_contents, options['truncate_contents'])

    if file_status != 'success':
        results['missing'] = True
        results['other files'] = os.listdir('.')
        results['optional'] = options['optional']
        return results

    results['contents'] = file_contents

    any_step_failed = False
    for step in steps:
        command = step.replace('$@', './' + filename)
        command = command.replace('$SUPPORT', supporting_dir)
        cmd, input_for_cmd = kinda_pipe_commands(command)
        status, compilation = run(cmd, input=input_for_cmd)

        results['compilation'].append({
            'command': command,
            'output': compilation,
            'status': status,
        })

        if status != 'success':
            any_step_failed = True
            break

    if any_step_failed or (not steps):
        return results

    tests = flatten([
        test_spec['commands']
        for test_spec in spec.get('tests', {})
        if test_spec['filename'] == filename
    ])

    for test in tests:
        if not test:
            continue

        test = test.replace('$@', './' + filename)
        test = test.replace('$SUPPORT', supporting_dir)
        test_cmd, input_for_test = kinda_pipe_commands(test)

        if exists(path_join(cwd, filename)):
            status, full_result = run(test_cmd,
                                      input=input_for_test,
                                      timeout=options['timeout'])

            result = unicode_truncate(full_result, options['truncate_output'])
            truncated = (full_result != result)

            results['result'].append({
                'command': test,
                'status': status,
                'output': result,
                'truncated': True if truncated else False,
                'truncated after': options['truncate_output'],
            })

        else:
            results['result'].append({
                'command': test,
                'error': True,
                'output': '{} could not be found.'.format(filename),
            })

    return results


def find_unmerged_branches():
    # approach taken from https://stackoverflow.com/a/3602022/2347774
    unmerged_branches = find_unmerged_branches_in_cwd()
    if not unmerged_branches:
        return False

    return unmerged_branches


def find_warnings():
    return {'unmerged branches': find_unmerged_branches()}


def markdownify_throws(spec_id, username, spec, basedir):
    cwd = os.getcwd()
    results = {
        'spec': spec_id,
        'student': username,
        'warnings': {},
        'files': OrderedDict(),
    }

    inputs = spec.get('inputs', [])
    supporting = path_join(basedir, 'data', 'supporting')
    for filename in inputs:
        in_path = path_join(supporting, spec_id, filename)
        out_path = path_join(cwd, filename)
        with open(in_path, 'rb') as infile:
            contents = infile.read()
        with open(out_path, 'wb') as outfile:
            outfile.write(contents)

    for file in spec['files']:
        filename = file['filename']
        steps = file['commands']
        options = file['options']
        result = process_file(filename, steps, options, spec, cwd, supporting)
        results['files'][filename] = result

    try:
        for file in spec['files']:
            os.remove('{}.exec'.format(file['filename']))
        for inputfile in inputs:
            os.remove(inputfile)
    except FileNotFoundError as e:
        pass

    results['warnings'] = find_warnings()
    return results


def markdownify(spec_id, username, spec, basedir):
    try:
        return markdownify_throws(spec_id, username, spec, basedir)
    except Exception as err:
        return {
            'spec': spec_id,
            'student': username,
            'warnings': {
                'Recording error': str(err),
            },
        }
