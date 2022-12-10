from ..common import chdir, run


def reset(student: str):
    with chdir(student):
        run(['git', 'checkout', 'main', '--quiet', '--force'])
