import requests
from unittest import mock

from stograde.toolkit.config import conf
from stograde.toolkit.find_update import get_all_versions, update_available


def test_get_all_versions():
    assert get_all_versions()[:12] == ['2.8.0', '2.8.2', '2.9.0', '2.9.1', '2.9.2',
                                       '3.0.0', '3.0.1', '3.1.0', '3.2.0',
                                       '4.0.0', '4.0.1', '4.0.2']


def test_get_all_versions_error():
    with mock.patch('requests.get', side_effect=requests.exceptions.ConnectionError()):
        assert get_all_versions() == []

    with mock.patch('requests.get', side_effect=requests.exceptions.Timeout()):
        assert get_all_versions() == []


@mock.patch('stograde.toolkit.find_update.version', '4.0.2')
def test_update_available_no_check_needed():
    with mock.patch.object(conf, 'needs_update_check', return_value=False):
        assert update_available() == ('4.0.2', None)


@mock.patch('stograde.toolkit.find_update.version', '4.0.2')
def test_update_available_version_not_present():
    with mock.patch.object(conf, 'needs_update_check', return_value=True):
        with mock.patch.object(conf, 'set_last_update_check'):
            with mock.patch('stograde.toolkit.find_update.get_all_versions', return_value=['1.0.0', '2.0.0']):
                assert update_available() == ('4.0.2', None)


@mock.patch('stograde.toolkit.find_update.version', '4.0.2')
def test_update_available_update_available():
    with mock.patch.object(conf, 'needs_update_check', return_value=True):
        with mock.patch.object(conf, 'set_last_update_check'):
            with mock.patch('stograde.toolkit.find_update.get_all_versions', return_value=['1.0.0', '4.0.2', '6.0.0']):
                assert update_available() == ('4.0.2', '6.0.0')


@mock.patch('stograde.toolkit.find_update.version', '4.0.2')
def test_update_available_no_update_available():
    with mock.patch.object(conf, 'needs_update_check', return_value=True):
        with mock.patch.object(conf, 'set_last_update_check'):
            with mock.patch('stograde.toolkit.find_update.get_all_versions', return_value=['1.0.0', '2.0.0', '4.0.2']):
                assert update_available() == ('4.0.2', None)
