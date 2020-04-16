import contextlib
import logging
import os
from pathlib import Path

from stograde.common import run
from stograde.student import clone_url, clone_student
from stograde.toolkit.check_dependencies import is_stogit_known_host
from test.common.test_find_unmerged_branches_in_cwd import touch


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


def test_clone_student(tmpdir, caplog):
    with stogit_as_known_host():
        with tmpdir.as_cwd():
            with caplog.at_level(logging.DEBUG):
                # Technically this clone will fail, but what we're checking is that the url is calculated correctly
                # and that the clone_url function is properly called
                clone_student(student='nonexistent', base_url='git@stogit.cs.stolaf.edu:sd/s20')

    log_messages = [log.msg for log in caplog.records]

    assert log_messages == ["Cloning nonexistent's repository",
                            'cloning git@stogit.cs.stolaf.edu:sd/s20/nonexistent.git']


def test_clone_url(tmpdir, caplog):
    with tmpdir.as_cwd():
        with caplog.at_level(logging.INFO):
            clone_url('https://github.com/StoDevX/cs251-specs.git')
        assert os.path.exists('cs251-specs')

    log_messages = [log.msg for log in caplog.records]

    assert len(log_messages) == 1

    assert log_messages[0] == 'cloning https://github.com/StoDevX/cs251-specs.git'

    for log in caplog.records:
        assert log.levelname == 'INFO'


def test_clone_url_into(tmpdir, caplog):
    with tmpdir.as_cwd():
        with caplog.at_level(logging.INFO):
            clone_url('https://github.com/StoDevX/cs251-specs.git', 'another_dir')
        assert os.path.exists('another_dir')

    log_messages = [log.msg for log in caplog.records]

    assert len(log_messages) == 1

    assert log_messages[0] == 'cloning https://github.com/StoDevX/cs251-specs.git into another_dir'

    for log in caplog.records:
        assert log.levelname == 'INFO'


def test_clone_url_permission_denied(tmpdir, capsys):
    with tmpdir.as_cwd():
        cwd = os.getcwd()
        key_file = os.path.join(cwd, 'totally_a_private_key')

        run(['ssh-keygen', '-b', '8192', '-n', '""', '-f', key_file])

        # Create a fake private key that can't possibly be registered with StoGit
        # (if somehow having an empty private key works, then something's really wrong with StoGit's security)
        # with open(os.path.join(cwd, 'totally_a_private_key'), 'w') as key:
        #     key.write('-----BEGIN RSA PRIVATE KEY-----\n-----END RSA PRIVATE KEY-----\n')
        # os.chmod(os.path.join(cwd, 'totally_a_private_key'), 0o600)  # SSH complains otherwise
        # Tell git to use our new 'private key'
        ssh_command = os.getenv('GIT_SSH_COMMAND', '')
        os.environ['GIT_SSH_COMMAND'] = 'ssh -i {}'.format(key_file)

        try:
            with stogit_as_known_host():
                clone_url('git@stogit.cs.stolaf.edu:sd/s20/narvae1.git')
            raise AssertionError
        except SystemExit:
            pass
        finally:
            os.environ['GIT_SSH_COMMAND'] = ssh_command

    _, err = capsys.readouterr()

    assert err == 'Permission denied when cloning from git@stogit.cs.stolaf.edu:sd/s20/narvae1.git\n' \
                  'Make sure that this SSH key is registered with StoGit.\n'
