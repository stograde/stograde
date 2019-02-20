import subprocess
import copy
import pty
import io
import os


def run(cmd, *, interact=False, **kwargs):
    if interact:
        return run_interactive(cmd)
    return run_static(cmd, **kwargs)


def run_interactive(cmd):
    status = 'success'
    result = None

    print('Recording {}. Send EOF (^D) to end.'.format(cmd), end='\n\n')

    # This is mostly taken from the stdlib's `pty` docs
    with io.BytesIO() as script:
        def read(fd):
            data = os.read(fd, 1024)
            script.write(data)
            return data

        # TODO: update this with try/except clauses as we find exceptions
        pty.spawn(cmd, read)

        try:
            result = script.getvalue().decode(encoding='utf-8')
        except UnicodeDecodeError:
            result = script.getvalue().decode(encoding='cp437')

    print('\nSubmission recording completed.')

    runagain = input('Do you want to run the submission again? [y/N]: ')
    again = runagain.lower().startswith('y')

    return (status, result, again)


def run_static(cmd, input_data=None, timeout=None):
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

    return (status, result, False)


# This is to catch glibc errors, because it prints to /dev/tty
# instead of stderr. See https://stackoverflow.com/a/27797579
def copy_env():
    env = copy.copy(os.environ)
    env["LIBC_FATAL_STDERR_"] = "1"
    return env
