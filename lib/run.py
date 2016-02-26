#!/usr/bin/env python3
import sys
import os
from subprocess import PIPE, STDOUT, check_output, \
                       CalledProcessError, TimeoutExpired


def run_command(cmd, *args, status=True, stdout=PIPE, input=None, timeout=None, **kwargs):
    if type(cmd) == str:
        cmd = str.split(' ')

    try:
        status = 'success'
        result = check_output(
            cmd,
            *args,
            stderr=STDOUT,
            timeout=timeout,
            input=input,
            **kwargs)

    except CalledProcessError as err:
        status = 'process error'
        result = err.output

    except TimeoutExpired as err:
        status = 'timed out after %s seconds' % timeout
        result = err.output

    except FileNotFoundError as err:
        status = 'not found'
        result = repr(err)

    except ProcessLookupError as err:
        try:
            status, result = run_command(*args, status=status, **kwargs)
        except:
            status = 'process error'
            result = repr(err)

    try:
        if type(result) is not str:
            result = str(result, 'utf-8')
    except UnicodeDecodeError as err:
        result = str(result, 'cp437')

    return (status, result)


if __name__ == '__main__':
    filePath = sys.argv[1]
    print(run_command([filePath]))
