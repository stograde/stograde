from cs251tk.common import chdir
from cs251tk.common import run


def stash(student, args):
    with chdir(student):
        if not args['no_update'] and has_changed_files():
            run(['git', 'stash', '-u'])
            run(['git', 'stash', 'clear'])


def has_changed_files():
    _, output = run(['git', 'status', '--porcelain'])
    return bool(output)
