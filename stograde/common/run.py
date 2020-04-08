import copy
import io
import os
import pty
import subprocess
from typing import List, Optional, Tuple

from ..common.run_status import RunStatus


def run(cmd: List[str],
        *,
        interact: bool = False,
        input_data: Optional[bytes] = None,
        timeout: Optional[float] = None) -> Tuple[RunStatus, str, bool]:
    if interact:
        return run_interactive(cmd)
    else:
        return run_static(cmd, input_data, timeout)


def run_interactive(cmd: List[str]) -> Tuple[RunStatus, str, bool]:
    status = RunStatus.SUCCESS
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

    return status, result, again


def run_static(cmd: List[str],
               input_data: Optional[bytes] = None,
               timeout: Optional[int] = None) -> Tuple[RunStatus, str, bool]:
    status = RunStatus.SUCCESS
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
        status = RunStatus.CALLED_PROCESS_ERROR
        result = err.output if err.output else str(err)

    except subprocess.TimeoutExpired as err:
        status = RunStatus.TIMEOUT_EXPIRED
        result = err.output if err.output else str(err)

    except FileNotFoundError as err:
        status = RunStatus.FILE_NOT_FOUND
        result = str(err)

    except ProcessLookupError as err:
        try:
            status, result, _ = run(cmd, input_data=input_data, timeout=timeout)
        except:
            status = RunStatus.PROCESS_LOOKUP_ERROR
            result = str(err)

    if hasattr(result, 'stdout'):
        result = result.stdout

    try:
        if not isinstance(result, str):
            result = str(result, 'utf-8')
    except UnicodeDecodeError:
        result = str(result, 'cp437')

    return status, result, False


# This is to catch glibc errors, because it prints to /dev/tty
# instead of stderr. See https://stackoverflow.com/a/27797579
def copy_env():
    env = copy.copy(os.environ)
    env["LIBC_FATAL_STDERR_"] = "1"
    return env
