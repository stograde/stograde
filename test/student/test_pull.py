import logging
import os

from stograde.student import pull, clone_url


def test_pull_success(tmpdir, caplog):
    with tmpdir.as_cwd():
        clone_url('https://github.com/stograde/cs251-specs.git')
        with caplog.at_level(logging.DEBUG):
            pull('cs251-specs')

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {("Pulling cs251-specs's repository", 'DEBUG')}


def test_pull_fail(tmpdir, capsys):
    with tmpdir.as_cwd():
        os.makedirs('not_a_git_repo')
        pull('not_a_git_repo')

    _, err = capsys.readouterr()

    assert err == ('Student directory not_a_git_repo is not a git repository\n'
                   'Try running "stograde repo reclone"\n')
