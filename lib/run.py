#!/usr/bin/env python3
import shlex
import copy
import sys
import os
from subprocess import STDOUT, check_output, \
                       CalledProcessError, TimeoutExpired

# This env stuff is to catch glibc errors, because
# it apparently prints to /dev/tty instead of stderr.
# (see http://stackoverflow.com/a/27797579)
ENV = copy.copy(os.environ)
ENV["LIBC_FATAL_STDERR_"] = "1"


def run(cmd, *args, input=None, timeout=None, **kwargs):
    if isinstance(cmd, str):
        cmd = shlex.split(str)

    try:
        status = 'success'
        result = check_output(
            cmd,
            *args,
            stderr=STDOUT,
            timeout=timeout,
            input=input,
            env=ENV,
            **kwargs)

    except CalledProcessError as err:
        status = 'called process error'
        result = err.output if err.output else str(err)

    except TimeoutExpired as err:
        status = 'timed out after {} seconds'.format(timeout)
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
        if not isinstance(result, str):
            result = str(result, 'utf-8')
    except UnicodeDecodeError as err:
        result = str(result, 'cp437')

    return (status, result)


if __name__ == '__main__':
    print(run([sys.argv[1]]))
