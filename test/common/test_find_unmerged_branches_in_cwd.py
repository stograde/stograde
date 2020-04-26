import os

from stograde.common.find_unmerged_branches_in_cwd import find_unmerged_branches_in_cwd
from test.utils import git, touch

_dir = os.path.dirname(os.path.realpath(__file__))


def test_find_unmerged_branches_in_cwd(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('file1')
        git('add', 'file1')
        git('commit', '-m', 'initial')

        git('checkout', '-b', 'branch')

        touch('file2')
        git('add', 'file2')
        git('commit', '-m', 'newcommit')

        git('checkout', 'master')

        assert find_unmerged_branches_in_cwd() == ['branch']

        git('merge', 'branch')

        assert find_unmerged_branches_in_cwd() == []
