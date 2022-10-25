from stograde.student import reset
from test.utils import git, touch


def test_reset(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('symbolic-ref', 'HEAD', 'refs/heads/main')  # Workaround for older versions of git without default main
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')
        touch('test_file.txt')
        git('add', 'test_file.txt')
        git('commit', '-m', '"First commit"')
        _, out, _ = git('branch')
        assert out == '* main\n'
        git('branch', 'another_branch')
        git('checkout', 'another_branch')
        _, out, _ = git('branch')
        assert out == '* another_branch\n  main\n'
        reset('.')
        _, out, _ = git('branch')
        assert out == '  another_branch\n* main\n'
