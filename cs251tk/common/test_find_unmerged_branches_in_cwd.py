from .find_unmerged_branches_in_cwd import find_unmerged_branches_in_cwd
from .run import run


def git(cmd, *args):
    return run(['git', cmd, *args])


def touch(file):
    return run(['touch', file])


def test_find_unmerged_branches_in_cwd(tmpdir):
    with tmpdir.as_cwd():
        git('init')

        touch('file1')
        git('add', 'file1')
        git('commit', '-m', 'initial')

        git('checkout', '-b', 'branch')

        touch('file2')
        git('add', 'file2')
        git('commit', '-m', 'newcommit')

        git('checkout', 'master')

        assert find_unmerged_branches_in_cwd() == ['branch']
