import os
import sys
from unittest import mock

from stograde.toolkit.check_dependencies import check_git_installed, check_stogit_known_host, \
    check_dependencies


def test_check_dependencies_passing(capsys):
    with mock.patch('stograde.toolkit.check_dependencies.is_stogit_known_host', return_value=True):
        try:
            # Note that this test requires that git is actually installed on the system,
            # which I think should always be true
            check_dependencies()
        except SystemExit:
            raise AssertionError

        _, err = capsys.readouterr()
        assert not err


def test_check_stogit_known_host_failing(capsys):
    with mock.patch('stograde.toolkit.check_dependencies.is_stogit_known_host', return_value=False):
        try:
            check_stogit_known_host()
            print(capsys.readouterr()[1], file=sys.stderr)
            raise AssertionError
        except SystemExit:
            pass

    _, err = capsys.readouterr()
    assert err == ('stogit.cs.stolaf.edu not in known hosts\n'
                   'Run "ssh-keyscan stogit.cs.stolaf.edu >> ~/.ssh/known_hosts" to fix\n')


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
