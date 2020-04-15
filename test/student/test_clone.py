import logging
import os

from stograde.student import clone_url, clone_student
from test.common.test_find_unmerged_branches_in_cwd import touch


def test_clone_student(tmpdir, caplog):
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

        # Create a fake private key that can't possibly be registered with StoGit
        # (if somehow having an empty private key works, then something's really wrong with StoGit's security)
        touch(os.path.join(cwd, 'totally_a_private_key'))
        os.chmod(os.path.join(cwd, 'totally_a_private_key'), 0o600)  # SSH complains otherwise
        # Tell git to use our new 'private key'
        ssh_command = os.getenv('GIT_SSH_COMMAND', '')
        os.environ['GIT_SSH_COMMAND'] = 'ssh -i {}'.format(os.path.join(cwd, 'totally_a_private_key'))

        try:
            clone_url('git@stogit.cs.stolaf.edu:sd/s20/narvae1.git')
            raise AssertionError
        except SystemExit:
            pass
        finally:
            os.environ['GIT_SSH_COMMAND'] = ssh_command

    _, err = capsys.readouterr()

    assert err == 'Permission denied when cloning from git@stogit.cs.stolaf.edu:sd/s20/narvae1.git\n' \
                  'Make sure that this SSH key is registered with StoGit.\n'
