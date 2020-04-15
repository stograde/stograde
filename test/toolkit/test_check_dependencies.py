import os

from stograde.toolkit.check_dependencies import check_git_installed


def test_check_git_installed_passing():
    try:
        check_git_installed()
    except SystemExit:
        raise AssertionError


def test_check_git_installed_failing(capsys):
    path = os.getenv('PATH')
    os.environ['PATH'] = ''

    try:
        check_git_installed()
    except SystemExit:
        pass
    finally:
        os.environ['PATH'] = path

    _, err = capsys.readouterr()

    assert err == 'git is not installed\nInstall git to continue\n'
