import os
import sys
import subprocess


def run(*args, status=True, **kwargs):
    try:
        code = 0
        result = subprocess.check_output(
            *args,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
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

    # print(result)

    return (code, result) if status else result
