import os
from unittest import mock

from stograde.toolkit.check_dependencies import check_git_installed


def test_check_git_installed_passing():
    try:
        check_git_installed()
    except SystemExit:
        raise AssertionError


def test_check_git_installed_failing(capsys):
    try:
        # If the command line doesn't have a valid path
        # then there's no way it can find the git executable
        with mock.patch.dict(os.environ, {'PATH': ''}):
            check_git_installed()
        raise AssertionError
    except SystemExit:
        pass

    _, err = capsys.readouterr()

    assert err == ('git is not installed\n'
                   'Install git to continue\n')
