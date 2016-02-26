#!/usr/bin/env python3
import subprocess
import sys
import os


def run_command(*args, status=True, **kwargs):
    try:
        code = 0
        result = subprocess.check_output(
            *args,
            stderr=subprocess.STDOUT,
            **kwargs)

    except subprocess.CalledProcessError as err:
        code = 1
        result = err.output

    except subprocess.TimeoutExpired as err:
        code = 1
        result = err.output

    except FileNotFoundError as err:
        code = 1
        result = repr(err)

    except ProcessLookupError as err:
        try:
            code, result = run_command(*args, status=status, **kwargs)
        except:
            code = 1
            result = repr(err)

    try:
        result = str(result, 'utf-8')
    except UnicodeDecodeError as err:
        result = str(result, 'cp437')

    return (code, result) if status else result


if __name__ == '__main__':
    filePath = sys.argv[1]
    print(run_command([filePath]))
