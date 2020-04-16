from stograde.student import reset
from test.common.test_find_unmerged_branches_in_cwd import git, touch


def test_reset(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')
        touch('test_file.txt')
        git('add', 'test_file.txt')
        git('commit', '-m', '"First commit"')
        _, out, _ = git('branch')
        assert out == '* master\n'
        git('branch', 'another_branch')
        git('checkout', 'another_branch')
        _, out, _ = git('branch')
        assert out == '* another_branch\n  master\n'
        reset('.')
        _, out, _ = git('branch')
        assert out == '  another_branch\n* master\n'
