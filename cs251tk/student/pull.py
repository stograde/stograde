from cs251tk.common import chdir
from cs251tk.common import run


def pull(student, args):
    with chdir(student):
        if not args['no_update']:
            run(['git', 'pull', '--quiet', 'origin', 'master'])

