from stograde.common import chdir
from stograde.common import run


def reset(student):
    with chdir(student):
        run(['git', 'checkout', 'master', '--quiet', '--force'])
