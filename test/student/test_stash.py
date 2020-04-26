import logging
import os

from stograde.student import stash
from test.utils import git, touch


def test_stash(tmpdir, caplog):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('test_file.txt')
        git('add', 'test_file.txt')
        git('commit', '-m', '"First commit"')
        assert os.path.exists('test_file.txt')
        assert not os.path.exists('test_file2.txt')

        touch('test_file2.txt')
        assert os.path.exists('test_file.txt')
        assert os.path.exists('test_file2.txt')

        with caplog.at_level(logging.DEBUG):
            stash('.')

        assert os.path.exists('test_file.txt')
        assert not os.path.exists('test_file2.txt')

    log_messages = [log.msg for log in caplog.records]

    assert log_messages == ["Stashing .'s repository"]
