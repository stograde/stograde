from cs251tk.common import chdir
from cs251tk.common import run


def reset(student):
    with chdir(student):
        run(['git', 'checkout', 'master', '--quiet', '--force'])
