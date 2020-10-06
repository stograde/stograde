import datetime
import os
from unittest import mock

import pytest

from stograde.common import chdir
from stograde.toolkit.config import Config

_dir = os.path.dirname(os.path.realpath(__file__))


def test_setup(tmpdir):
    with tmpdir.as_cwd():
        assert not os.path.exists('stograde.ini')
        with mock.patch('stograde.toolkit.config.Config._filename', 'stograde.ini'):
            Config()
        assert os.path.exists('stograde.ini')


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'config'))
def test_get_last_update_check(datafiles):
    with chdir(str(datafiles)):
        with mock.patch('stograde.toolkit.config.Config._filename', 'stograde.ini'):
            c = Config()
            assert c.get_last_update_check() == datetime.datetime(2020, 8, 30, 11, 59, 39, 378987)


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'config'))
def test_set_last_update_check(datafiles):
    with chdir(str(datafiles)):
        with open('stograde.ini') as file:
            old_contents = file.read()
            file.close()
        with mock.patch('stograde.toolkit.config.Config._filename', 'stograde.ini'):
            Config().set_last_update_check()
        with open('stograde.ini') as file:
            new_contents = file.read()
            file.close()

        assert old_contents != new_contents


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'config'))
def test_needs_update_check(datafiles):
    with chdir(str(datafiles)):
        with mock.patch('stograde.toolkit.config.Config._filename', 'stograde.ini'):
            c = Config()
            assert c.needs_update_check()
            c.set_last_update_check()
            assert not c.needs_update_check()
