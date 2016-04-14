#!/usr/bin/env python3

import sys
import os
from collections import OrderedDict
from os.path import exists, join as path_join
from .find_unmerged_branches_in_cwd import find_unmerged_branches_in_cwd
from .flatten import flatten
from .run import run


def unicode_truncate(s, length, encoding='utf-8'):
    encoded = s.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')


def kinda_pipe_commands(cmd_string):
    cmds = cmd_string.split(' | ')

    input_for_cmd = None
    for cmd in cmds[:-1]:
        # decode('unicode_escape') de-escapes the backslash-escaped strings.
        # like, it turns the \n from "echo Hawken \n 26" into an actual newline,
        # like a shell would.
        cmd = bytes(cmd, 'utf-8').decode('unicode_escape')
        cmd = cmd.split(' ')

        status, input_for_cmd = run(cmd, input=input_for_cmd)
        input_for_cmd = input_for_cmd.encode('utf-8')

    final_cmd = cmds[-1].split(' ')

    return (final_cmd, input_for_cmd)


def process_file(filename, steps, spec, cwd):
    steps = steps if type(steps) is list else [steps]

    options = {
        'timeout': 4,
        'truncate_after': 10000,  # 10K
        'truncate_contents': False,
        'optional': False,
    }
    options.update(spec.get('options', {}).get(filename, {}))

    results = {
        'missing': False,
        'compilation': [],
        'result': [],
    }

    file_status, file_contents = run(['cat', filename])
    if file_status == 'success':
        _, last_edit = run(['git', 'log',
                            '-n', '1',
                            r'--pretty=format:%cd',
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

    inputs = spec.get('inputs', {})

    tests = spec.get('tests', {}).get(filename, [])
    if type(tests) is not list:
        tests = [tests]

    for test in tests:
        if not test:
            continue

        test = test.replace('$@', './%s' % filename)
        test_cmd, input_for_test = kinda_pipe_commands(test)

        if exists(path_join(cwd, filename)):
            status, full_result = run(test_cmd,
                                      input=input_for_test,
                                      timeout=options['timeout'])

            result = unicode_truncate(full_result, options['truncate_after'])
            truncated = (full_result != result)
            truncate_msg = 'output truncated after %d bytes' % (options['truncate_after']) \
                           if truncated else ''

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
    return {
        'unmerged branches': find_unmerged_branches(),
    }


def markdownify_throws(spec_id, username, spec):
    cwd = os.getcwd()
    results = {
        'spec': spec_id,
        'student': username,
        'warnings': {},
        'files': OrderedDict(),
    }

    inputs = spec.get('inputs', {})
    for filename, contents in inputs.items():
        with open(path_join(cwd, filename), 'w') as outfile:
            outfile.write(contents)

    files = [(filename, steps)
             for file in spec['files']
             for filename, steps in file.items()]

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
