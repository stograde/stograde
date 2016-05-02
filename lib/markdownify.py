import sys
import os
import shlex
from glob import glob
from collections import OrderedDict
from os.path import exists, join as path_join
from .find_unmerged_branches_in_cwd import find_unmerged_branches_in_cwd
from .specs import get_files_and_steps
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
    cmd = shlex.split(cmd)

    cmd = list(flatten([expand_chunk(c) for c in cmd]))

    return cmd


def kinda_pipe_commands(cmd_string):
    cmds = cmd_string.split(' | ')

    input_for_cmd = None
    for cmd in cmds[:-1]:
        cmd = process_chunk(cmd)
        _, input_for_cmd = run(cmd, input=input_for_cmd)
        input_for_cmd = input_for_cmd.encode('utf-8')

    final_cmd = process_chunk(cmds[-1])
    return (final_cmd, input_for_cmd)


def process_file(filename, steps, spec, cwd):
    steps = steps if isinstance(steps, list) else [steps]

    options = {
        'timeout': 4,
        'truncate_after': 10000,  # 10K
        'truncate_contents': False,
        'optional': False,
    }
    options.update(spec.get('options', {}).get(filename, {}))

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

    if options['truncate_contents']:
        file_contents = unicode_truncate(file_contents, options['truncate_contents'])

    if file_status != 'success':
        results['missing'] = True
        results['other files'] = os.listdir('.')
        results['optional'] = options['optional']
        return results

    results['contents'] = file_contents

    any_step_failed = False
    for step in steps:
        if step and not any_step_failed:
            command = step.replace('$@', filename)
            cmd, input_for_cmd = kinda_pipe_commands(command)
            status, compilation = run(cmd, input=input_for_cmd)

            results['compilation'].append({
                'command': command,
                'output': compilation,
                'status': status,
            })

            if status != 'success':
                any_step_failed = True

        elif any_step_failed:
            break

    if not steps or any_step_failed:
        return results

    tests = spec.get('tests', {}).get(filename, [])
    if not isinstance(tests, list):
        tests = [tests]

    for test in tests:
        if not test:
            continue

        test = test.replace('$@', './' + filename)
        test_cmd, input_for_test = kinda_pipe_commands(test)

        if exists(path_join(cwd, filename)):
            status, full_result = run(test_cmd,
                                      input=input_for_test,
                                      timeout=options['timeout'])

            result = unicode_truncate(full_result, options['truncate_after'])
            truncated = (full_result != result)

            results['result'].append({
                'command': test,
                'status': status,
                'output': result,
                'truncated': True if truncated else False,
                'truncated after': options['truncate_after'],
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


def markdownify_throws(spec_id, username, spec):
    cwd = os.getcwd()
    results = {
        'spec': spec_id,
        'student': username,
        'warnings': {},
        'files': OrderedDict(),
    }

    inputs = spec.get('inputs', [])
    for filename in inputs:
        # remember that we're currently in … a folder. frick.
        # can't assume that this is a child of the student's folder.
        # we'll start with that assumption, but it'll break on some of the labs.
        in_path = path_join(cwd, '..', '..', '..', 'supporting', spec_id, filename)
        out_path = path_join(cwd, filename)
        with open(in_path, 'rb') as infile:
            contents = infile.read()
        with open(out_path, 'wb') as outfile:
            outfile.write(contents)

    files = get_files_and_steps(spec)

    for filename, steps in files:
        result = process_file(filename, steps, spec, cwd)
        results['files'][filename] = result

    [run(['rm', '-f', file + '.exec']) for file, steps in files]
    [os.remove(path_join(cwd, inputfile)) for inputfile in inputs]

    results['warnings'] = find_warnings()
    return results


def markdownify(spec_id, username, spec):
    try:
        return markdownify_throws(spec_id, username, spec)
    except Exception as err:
        return {
            'spec': spec_id,
            'student': username,
            'warnings': {
                'Recording error': str(err),
            },
        }
