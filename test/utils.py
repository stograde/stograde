from stograde.common import run


def git(cmd, *args):
    return run(['git', cmd, *args])


def touch(file):
    return run(['touch', file])
