import os
import sys
import subprocess


def run(*args, status=True, **kwargs):
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
        code = 1
        result = repr(err)

    try:
        result = str(result, 'utf-8')
    except UnicodeDecodeError as err:
        result = str(result, 'cp437')
    # print(result)

    return (code, result) if status else result
