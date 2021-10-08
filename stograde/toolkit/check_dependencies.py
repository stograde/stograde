import sys

from ..common import run
from ..common.run_status import RunStatus


def check_dependencies():
    check_stogit_known_host()
    check_git_installed()


def is_stogit_known_host():
    status, output, _ = run(['ssh-keygen', '-F', 'stogit.cs.stolaf.edu'])
    if status is RunStatus.SUCCESS:
        return True
    return False


def check_stogit_known_host():
    if not is_stogit_known_host():
        print('stogit.cs.stolaf.edu not in known hosts', file=sys.stderr)
        print('Run "ssh-keyscan stogit.cs.stolaf.edu >> ~/.ssh/known_hosts" to fix', file=sys.stderr)
        sys.exit(1)


def is_git_installed():
    status, output, _ = run(['git', '--version'])
    if status is RunStatus.FILE_NOT_FOUND and 'No such file or directory' in output:
        return False
    return True


def check_git_installed():
    if not is_git_installed():
        print('git is not installed', file=sys.stderr)
        print('Install git to continue', file=sys.stderr)
        sys.exit(1)
