import sys

from ..common import run
from ..common.run_status import RunStatus


def check_dependencies():
    check_stogit_known_host()
    check_git_installed()


def check_stogit_known_host():
    status, output, _ = run(['ssh-keygen', '-F', 'stogit.cs.stolaf.edu'])
    if status is RunStatus.CALLED_PROCESS_ERROR and 'exit status 1' in output:
        print('stogit.cs.stolaf.edu not in known hosts\n'
              'Run ssh-keyscan stogit.cs.stolaf.edu >> ~/.ssh/known_hosts')
        sys.exit(1)


def check_git_installed():
    status, output, _ = run(['git', '--version'])
    if status is RunStatus.FILE_NOT_FOUND and 'No such file or directory' in output:
        print('git is not installed\n'
              'Install git to continue')
        sys.exit(1)
