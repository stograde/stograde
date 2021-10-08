import contextlib
import os
import sys
from pathlib import Path
from unittest import mock

from stograde.common import run
from stograde.toolkit.check_dependencies import check_git_installed, is_stogit_known_host, check_stogit_known_host, \
    check_dependencies


@contextlib.contextmanager
def stogit_as_known_host():
    modify_known_hosts = not is_stogit_known_host()

    try:
        if modify_known_hosts:
            _, out, _ = run(['ssh-keyscan', 'stogit.cs.stolaf.edu'])
            with (Path.home() / '.ssh' / 'known_hosts').open('a') as known_hosts:
                known_hosts.write(out)
                known_hosts.close()
        yield
    finally:
        if modify_known_hosts:
            run(['ssh-keygen', '-R', 'stogit.cs.stolaf.edu'])


@contextlib.contextmanager
def stogit_not_as_known_host():
    if not (Path.home() / '.ssh').exists():
        os.mkdir(Path.home() / '.ssh')
    if not (Path.home() / '.ssh' / 'known_hosts').exists():
        with open(Path.home() / '.ssh' / 'known_hosts', 'w'):
            pass
    modify_known_hosts = is_stogit_known_host()

    try:
        if modify_known_hosts:
            run(['ssh-keygen', '-R', 'stogit.cs.stolaf.edu'])
        yield
    finally:
        if modify_known_hosts:
            _, out, _ = run(['ssh-keyscan', 'stogit.cs.stolaf.edu'])
            with (Path.home() / '.ssh' / 'known_hosts').open('a') as known_hosts:
                known_hosts.write(out)
                known_hosts.close()


def test_check_dependencies_passing(capsys):
    with stogit_as_known_host():
        try:
            # Note that this test requires that git is actually installed on the system,
            # which I think should always be true
            check_dependencies()
        except SystemExit:
            raise AssertionError

        _, err = capsys.readouterr()
        assert not err


def test_check_stogit_known_host_failing(capsys):
    with stogit_not_as_known_host():
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
