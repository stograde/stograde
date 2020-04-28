import logging
import os
from unittest import mock

from stograde.common import run
from stograde.student import clone_url, clone_student
from test.toolkit.test_check_dependencies import stogit_as_known_host


def test_clone_student(tmpdir, caplog):
    with stogit_as_known_host():
        with tmpdir.as_cwd():
            with caplog.at_level(logging.DEBUG):
                # Technically this clone will fail, but what we're checking is that the url is calculated correctly
                # and that the clone_url function is properly called
                try:
                    clone_student(student='nonexistent', base_url='git@stogit.cs.stolaf.edu:sd/s20')
                except SystemExit:
                    pass

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {("Cloning nonexistent's repository", 'DEBUG'),
                            ('cloning git@stogit.cs.stolaf.edu:sd/s20/nonexistent.git', 'INFO')}


def test_clone_url(tmpdir, caplog):
    with tmpdir.as_cwd():
        with caplog.at_level(logging.INFO):
            clone_url('https://github.com/StoDevX/cs251-specs.git')
        assert os.path.exists('cs251-specs')

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('cloning https://github.com/StoDevX/cs251-specs.git', 'INFO')}


def test_clone_url_into(tmpdir, caplog):
    with tmpdir.as_cwd():
        with caplog.at_level(logging.INFO):
            clone_url('https://github.com/StoDevX/cs251-specs.git', 'another_dir')
        assert os.path.exists('another_dir')

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('cloning https://github.com/StoDevX/cs251-specs.git into another_dir', 'INFO')}


def test_clone_url_permission_denied(tmpdir, capsys):
    with tmpdir.as_cwd():
        cwd = os.getcwd()
        key_file = os.path.join(cwd, 'a_private_key')

        # Create a fake private key that can't possibly be registered with StoGit
        # (or at least it has a chance of being registered that is lower than
        #  the chance of Great Britain being wiped out by an asteroid in the same
        #  second that the key is generated, according to stackexchange:
        #  https://security.stackexchange.com/a/2947)
        run(['ssh-keygen', '-b', '8192', '-N', '', '-f', key_file])

        # Tell git to use our new 'private key'
        # We have to modify the environment directly instead of using mock.patch.dict
        # because git doesn't get its environment variables from os.environ
        # ssh_command = os.getenv('GIT_SSH_COMMAND', '')
        # os.environ['GIT_SSH_COMMAND'] = 'ssh -i {}'.format(key_file)

        try:
            with stogit_as_known_host():
                with mock.patch.dict(os.environ, {'GIT_SSH_COMMAND': 'ssh -i {}'.format(key_file)}):
                    clone_url('git@stogit.cs.stolaf.edu:sd/s20/narvae1.git')
            raise AssertionError
        except SystemExit:
            pass
        # finally:
        #     os.environ['GIT_SSH_COMMAND'] = ssh_command

    _, err = capsys.readouterr()

    assert err == ('Permission denied when cloning from git@stogit.cs.stolaf.edu:sd/s20/narvae1.git\n'
                   'Make sure that this SSH key is registered with StoGit.\n')
