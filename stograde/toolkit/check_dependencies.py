import sys

from ..common import run
from ..common.run_status import RunStatus


def check_dependencies():
    status, output, _ = run(['ssh-keygen', '-F', 'stogit.cs.stolaf.edu'])
    if status is RunStatus.CALLED_PROCESS_ERROR and 'exit status 1' in output:
        print('stogit.cs.stolaf.edu not in known hosts\n'
              '')
        sys.exit(1)
