#!/usr/bin/env python3
import shlex
import copy
import sys
import os
from subprocess import PIPE, STDOUT, check_output, \
                       CalledProcessError, TimeoutExpired

# This env stuff is to catch glibc errors, because
# it apparently prints to /dev/tty instead of stderr.
# (see http://stackoverflow.com/a/27797579)
env = copy.copy(os.environ)
env["LIBC_FATAL_STDERR_"] = "1"


def run(cmd, *args, stdout=PIPE, input=None, timeout=None, **kwargs):
    if type(cmd) == str:
        cmd = shlex.split(str)

    try:
        status = 'success'
        result = check_output(
            cmd,
            *args,
            stderr=STDOUT,
            timeout=timeout,
            input=input,
            env=env,
            **kwargs)

    except CalledProcessError as err:
        status = 'called process error'
        result = err.output if err.output else str(err)

    except TimeoutExpired as err:
        status = 'timed out after %s seconds' % timeout
        result = err.output if err.output else str(err)

    except FileNotFoundError as err:
        status = 'not found'
        result = str(err)

    except ProcessLookupError as err:
        try:
            status, result = run(*args, status=status, **kwargs)
        except:
            status = 'process lookup error'
            result = str(err)

    try:
        if type(result) is not str:
            result = str(result, 'utf-8')
    except UnicodeDecodeError as err:
        result = str(result, 'cp437')

    return (status, result)


if __name__ == '__main__':
    filePath = sys.argv[1]
    print(run([filePath]))
