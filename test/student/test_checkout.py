import logging
import os
from unittest import mock

import pytest

from stograde.common import chdir
from stograde.student import checkout_date
from test.utils import git, touch


@pytest.mark.skip
def test_checkout_date(tmpdir, caplog):
    with tmpdir.as_cwd():
        os.makedirs('student')
        with chdir('student'):
            git('init')
            git('symbolic-ref', 'HEAD', 'refs/heads/main')  # Workaround for older versions of git without default main
            git('config', 'user.email', 'an_email@email_provider.com')
            git('config', 'user.name', 'Some Random Name')

            touch('a_file.txt')
            git('add', 'a_file.txt')
            with mock.patch.dict(os.environ, {'GIT_COMMITTER_DATE': 'Tue Apr 21 12:28:03 2020 -0500'}):
                git('commit', '-m', '"Add file"')

            touch('b_file.txt')
            git('add', 'b_file.txt')
            with mock.patch.dict(os.environ, {'GIT_COMMITTER_DATE': 'Sat Apr 25 20:27:05 2020 -0500'}):
                git('commit', '-m', '"Add another file"')

        assert os.path.exists(os.path.join('student', 'a_file.txt'))
        assert os.path.exists(os.path.join('student', 'b_file.txt'))

        with caplog.at_level(logging.DEBUG):
            checkout_date('student', 'Apr 23 2020')

        assert os.path.exists(os.path.join('student', 'a_file.txt'))
        assert not os.path.exists(os.path.join('student', 'b_file.txt'))

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {("Checking out commits in student's repository before Apr 23 2020", 'DEBUG')}


@mock.patch('stograde.student.checkout.checkout_ref')
def test_checkout_date_no_date(mock_function):
    checkout_date('student', 'main', None)
    assert not mock_function.called
