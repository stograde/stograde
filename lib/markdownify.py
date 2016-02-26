#!/usr/bin/env python3

import sys
import os
from textwrap import indent
from .flatten import flatten
from .run import run_command, run_file


def indent4(string):
    return indent(string, '    ')


def markdownify(hw_number, username, spec, output_type=None, to=None):
    cwd = os.getcwd()
    results = []

    for filename, contents in spec.get('inputs', {}).items():
        with open(os.path.join(cwd, filename), 'w') as outfile:
            outfile.write(contents)

    files = [(filename, steps)
             for file in spec['files']
             for filename, steps in file.items()]

    for filename, steps in files:
        steps = steps if type(steps) is list else [steps]

        output = []
        header = '### ' + filename


        output.extend([header, '\n'])
        file_status, file_contents = run_command(['cat', filename])

        if file_status:
            output.append('**file %s does not exist**\n' % filename)
            output.append('`ls .` says that these files exist:\n')
            output.append(indent4('\n'.join(os.listdir('.'))) + '\n\n')
            results.append('\n'.join(output))
            continue

        output.extend(['**contents of %s**\n' % filename, indent4(file_contents)])
        output.append('\n')

        any_step_failed = False
        for step in steps:
            if step and not any_step_failed:
                command = step.replace('$@', filename)
                status, compilation = run_command(command.split())

                if compilation:
                    warnings_header = '**warnings: `%s`**\n' % (command)
                    output.extend([warnings_header, indent4(compilation)])
                else:
                    warnings_header = '**no warnings: `%s`**' % (command)
                    output.extend([warnings_header])

                if status:
                    any_step_failed = True

                output.append('\n')

            elif any_step_failed:
                break

        if not steps or any_step_failed:
            results.append('\n'.join(output))
            continue

        inputs = spec.get('inputs', {})

        tests = spec.get('tests', {}).get(filename, [])
        if type(tests) is not list:
            tests = [tests]

        for test in tests:
            if not test:
                continue
            test = test.replace('$@', './%s' % file)
            output.append('**results of %s**\n' % (file))
            if os.path.exists(file_loc):
                status, result = run_file(test, shell=True)
                output.extend(["`%s`\n" % test, indent4(result)])
            else:
                output.append('%s could not be found.\n' % filename)

            output.append('\n')

        output.extend(["\n\n"])

        results.append('\n'.join(output))

    [run_command(['rm', '-f', '%s.exec' % file]) for file, steps in files]
    [os.remove(os.path.join(cwd, inputfile)) for inputfile in spec.get('inputs', {})]

    return '# %s — %s \n\n%s' % (
        hw_number,
        username,
        ''.join(results))
