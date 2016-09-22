from cs251tk.common import chdir
from cs251tk.common import run


def pull(student, no_update):
    with chdir(student):
        if not no_update:
            run(['git', 'pull', '--quiet', 'origin', 'master'])
