import datetime
import os
import re
from unittest import mock

# noinspection PyProtectedMember
import pytest

from stograde.toolkit.gist import get_auth, post_gist


def test_get_auth():
    with mock.patch('builtins.input', return_value='user'):
        with mock.patch('getpass.getpass', return_value='userpass'):
            assert get_auth() == ('user', 'userpass')


def test_post_gist_bad_auth():
    with mock.patch('builtins.input', return_value='user'):
        with mock.patch('getpass.getpass', return_value='userpass'):
            assert post_gist('describe', {'testFile.md': {'content': 'fileContents'}}) == '"Bad credentials"'


@pytest.mark.skipif(os.getenv('GIST_USER') is None, reason='Cannot run test without gist username')
@pytest.mark.skipif(os.getenv('GIST_KEY') is None, reason='Cannot run test without gist key')
def test_post_gist():
    with mock.patch('builtins.input', return_value=os.getenv('GIST_USER')):
        with mock.patch('getpass.getpass', return_value=os.getenv('GIST_KEY')):
            assert re.compile(r"^https://gist.github.com/.*$").match(
                post_gist('Testing StoGrade gist upload',
                          {'stogradeTest-{}.md'.format(datetime.date.today()): {'content': 'fileContents'}})
            )
