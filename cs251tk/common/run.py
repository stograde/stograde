import subprocess
import copy
import os


def run(cmd, input_data=None, timeout=None, interact=False):
    status = 'success'
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            input=input_data,
            env=copy_env(),
            check=True)

    except subprocess.CalledProcessError as err:
        status = 'called process error'
        result = err.output if err.output else str(err)

    except subprocess.TimeoutExpired as err:
        status = 'timed out after {} seconds'.format(timeout)
        result = err.output if err.output else str(err)

    except FileNotFoundError as err:
        status = 'not found'
        result = str(err)

    except ProcessLookupError as err:
        try:
            status, result = run(cmd, input_data=input_data, timeout=timeout)
        except:
            status = 'process lookup error'
            result = str(err)

    if hasattr(result, 'stdout'):
        result = result.stdout

    try:
        if not isinstance(result, str):
            result = str(result, 'utf-8')
    except UnicodeDecodeError:
        result = str(result, 'cp437')

    return (status, result)


# This is to catch glibc errors, because it prints to /dev/tty
# instead of stderr. See https://stackoverflow.com/a/27797579
def copy_env():
    env = copy.copy(os.environ)
    env["LIBC_FATAL_STDERR_"] = "1"
    return env
