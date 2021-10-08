import logging
import os
import sys

import pytest
from unittest import mock

from stograde.common import run
from stograde.common.run_status import RunStatus
from stograde.student import clone_url, clone_student
from test.toolkit.test_check_dependencies import stogit_as_known_host
from test.utils import remove_hostkeys_foreach_failed


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

        try:
            with stogit_as_known_host():
                with mock.patch.dict(os.environ, {'GIT_SSH_COMMAND': 'ssh -i {}'.format(key_file)}):
                    clone_url('git@stogit.cs.stolaf.edu:sd/s20/narvae1.git')
            print(capsys.readouterr()[1], file=sys.stderr)
            raise AssertionError
        except SystemExit:
            pass

    _, err = capsys.readouterr()

    assert remove_hostkeys_foreach_failed(err) == \
           ('Permission denied when cloning from git@stogit.cs.stolaf.edu:sd/s20/narvae1.git\n'
            'Make sure that this SSH key is registered with StoGit.\n')


def test_clone_url_repo_not_found(tmpdir, capsys):
    with stogit_as_known_host():
        with mock.patch('stograde.student.clone.run',
                        return_value=(RunStatus.CALLED_PROCESS_ERROR,
                                      ("Cloning into 'nonexistent'...\n"
                                       '> GitLab: The project you were looking for could not be found.\n'
                                       'fatal: Could not read from remote repository.\n\n'
                                       'Please make sure you have the correct access rights'
                                       'and the repository exists.\n'),
                                      False)):
            with tmpdir.as_cwd():
                try:
                    clone_student(student='nonexistent', base_url='git@stogit.cs.stolaf.edu:sd/s20')
                except SystemExit:
                    pass

    _, err = capsys.readouterr()

    assert remove_hostkeys_foreach_failed(err) == \
           'Could not find repository git@stogit.cs.stolaf.edu:sd/s20/nonexistent.git\n'
