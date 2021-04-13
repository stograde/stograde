import datetime
import os
import re
import textwrap
from unittest import mock

import pytest
# noinspection PyPackageRequirements
from oauthlib.oauth2 import InvalidClientError

from stograde.common import chdir
from stograde.drive.drive import authenticate_drive, get_all_files, get_assignment_files, group_files, create_line, \
    format_file_group, request_files
from stograde.drive.drive_result import DriveResult

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_authenticate_drive(datafiles, capsys):
    with chdir(str(datafiles)):
        with mock.patch('google_auth_oauthlib.flow.input', return_value='n'):
            try:
                authenticate_drive()
            except InvalidClientError:
                pass

    out, _ = capsys.readouterr()

    assert re.compile(
        'Please visit this URL to authorize this application: '
        r'https://accounts\.google\.com/o/oauth2/auth'
        r'\?response_type=code'
        r'&client_id=a-test-project\.apps\.googleusercontent\.com'
        r'&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2\.0%3Aoob'
        r'&scope=https%3A%2F%2Fwww\.googleapis\.com%2Fauth%2Fdrive\.metadata\.readonly'
        r'&state=.*'
        '&prompt=consent'
        '&access_type=offline\n').match(out)


def test_authenticate_drive_no_client_secret_json(tmpdir, capsys):
    with tmpdir.as_cwd():
        try:
            authenticate_drive()
            raise AssertionError
        except SystemExit:
            pass

    _, err = capsys.readouterr()

    assert err == ('client_secret.json is required for stograde drive functionality.\n'
                   'Follow the steps at https://github.com/StoDevX/stograde/blob/master/docs/DRIVE.md '
                   'to create the file.\n'
                   'If you have already created it, please make sure it is located in the directory where you are '
                   'running stograde.\n')


response = {'files': [{'createdTime': '2020-09-16T15:54:33.035Z',
                       'name': 'Copy of Lab 9',
                       'owners': [{'displayName': 'A Student',
                                   'emailAddress': 'student1@stolaf.edu',
                                   'kind': 'drive#user',
                                   'me': False,
                                   'permissionId': '#####'}],
                       'permissions': [{'deleted': False,
                                        'displayName': 'ta-group',
                                        'emailAddress': 'ta-group@stolaf.edu',
                                        'id': '#####',
                                        'kind': 'drive#permission',
                                        'role': 'writer',
                                        'type': 'group'},
                                       {'deleted': False,
                                        'displayName': 'A Student',
                                        'emailAddress': 'student1@stolaf.edu',
                                        'id': '#####',
                                        'kind': 'drive#permission',
                                        'role': 'owner',
                                        'type': 'user'}],
                       'webViewLink': 'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'},
                      {'createdTime': '2020-09-16T20:24:10.734Z',
                       'name': 'Copy of Lab 9',
                       'owners': [{'displayName': 'A Student',
                                   'emailAddress': 'student2@stolaf.edu',
                                   'kind': 'drive#user',
                                   'me': False,
                                   'permissionId': '#####'}],
                       'permissions': [{'deleted': False,
                                        'displayName': 'ta-group',
                                        'emailAddress': 'ta-group@stolaf.edu',
                                        'id': '#####',
                                        'kind': 'drive#permission',
                                        'role': 'writer',
                                        'type': 'group'},
                                       {'deleted': False,
                                        'displayName': 'A Student',
                                        'emailAddress': 'student2@stolaf.edu',
                                        'id': '#####',
                                        'kind': 'drive#permission',
                                        'role': 'owner',
                                        'type': 'user'}],
                       'webViewLink': 'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'},
                      {'createdTime': '2020-09-16T15:54:59.679Z',
                       'name': 'Copy of Lab 8',
                       'owners': [{'displayName': 'A Student',
                                   'emailAddress': 'student3@stolaf.edu',
                                   'kind': 'drive#user',
                                   'me': False,
                                   'permissionId': '#####'}],
                       'permissions': [{'deleted': False,
                                        'displayName': 'ta-group',
                                        'emailAddress': 'ta-group@stolaf.edu',
                                        'id': '#####',
                                        'kind': 'drive#permission',
                                        'role': 'writer',
                                        'type': 'group'},
                                       {'deleted': False,
                                        'displayName': 'A Student',
                                        'emailAddress': 'student3@stolaf.edu',
                                        'id': '#####',
                                        'kind': 'drive#permission',
                                        'role': 'owner',
                                        'type': 'user'}],
                       'webViewLink': 'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk'}]}

response_token = {'files': [{'createdTime': '2020-09-16T15:54:33.035Z',
                             'name': 'Copy of Lab 9',
                             'owners': [{'displayName': 'A Student',
                                         'emailAddress': 'student1@stolaf.edu',
                                         'kind': 'drive#user',
                                         'me': False,
                                         'permissionId': '#####'}],
                             'permissions': [{'deleted': False,
                                              'displayName': 'ta-group',
                                              'emailAddress': 'ta-group@stolaf.edu',
                                              'id': '#####',
                                              'kind': 'drive#permission',
                                              'role': 'writer',
                                              'type': 'group'},
                                             {'deleted': False,
                                              'displayName': 'A Student',
                                              'emailAddress': 'student1@stolaf.edu',
                                              'id': '#####',
                                              'kind': 'drive#permission',
                                              'role': 'owner',
                                              'type': 'user'}],
                             'webViewLink': 'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'},
                            {'createdTime': '2020-09-16T20:24:10.734Z',
                             'name': 'Copy of Lab 9',
                             'owners': [{'displayName': 'A Student',
                                         'emailAddress': 'student2@stolaf.edu',
                                         'kind': 'drive#user',
                                         'me': False,
                                         'permissionId': '#####'}],
                             'permissions': [{'deleted': False,
                                              'displayName': 'ta-group',
                                              'emailAddress': 'ta-group@stolaf.edu',
                                              'id': '#####',
                                              'kind': 'drive#permission',
                                              'role': 'writer',
                                              'type': 'group'},
                                             {'deleted': False,
                                              'displayName': 'A Student',
                                              'emailAddress': 'student2@stolaf.edu',
                                              'id': '#####',
                                              'kind': 'drive#permission',
                                              'role': 'owner',
                                              'type': 'user'}],
                             'webViewLink': 'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'},
                            {'createdTime': '2020-09-16T15:54:59.679Z',
                             'name': 'Copy of Lab 8',
                             'owners': [{'displayName': 'A Student',
                                         'emailAddress': 'student3@stolaf.edu',
                                         'kind': 'drive#user',
                                         'me': False,
                                         'permissionId': '#####'}],
                             'permissions': [{'deleted': False,
                                              'displayName': 'ta-group',
                                              'emailAddress': 'ta-group@stolaf.edu',
                                              'id': '#####',
                                              'kind': 'drive#permission',
                                              'role': 'writer',
                                              'type': 'group'},
                                             {'deleted': False,
                                              'displayName': 'A Student',
                                              'emailAddress': 'student3@stolaf.edu',
                                              'id': '#####',
                                              'kind': 'drive#permission',
                                              'role': 'owner',
                                              'type': 'user'}],
                             'webViewLink': 'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk'}],
                  'nextPageToken': 'a-token'}


class MockService:

    # noinspection PyPep8Naming
    def __init__(self):
        self.q = ''
        self.pageSize = -1
        self.fields = ''
        self.pageToken = ''

    def files(self):
        return self

    # noinspection PyPep8Naming,PyUnusedLocal
    def list(self, q, pageSize, fields, pageToken):
        self.q = q

        self.pageToken = pageToken
        return self

    # noinspection PyMethodMayBeStatic
    def execute(self):
        return response


def test_request_files_no_token():
    mock_service = MockService()
    date = datetime.date(2020, 4, 12)
    files, token = request_files(mock_service, None, 'an_email@stolaf.edu', date)
    assert files == [{'createdTime': '2020-09-16T15:54:33.035Z',
                      'name': 'Copy of Lab 9',
                      'owners': [{'displayName': 'A Student',
                                  'emailAddress': 'student1@stolaf.edu',
                                  'kind': 'drive#user',
                                  'me': False,
                                  'permissionId': '#####'}],
                      'permissions': [{'deleted': False,
                                       'displayName': 'ta-group',
                                       'emailAddress': 'ta-group@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'writer',
                                       'type': 'group'},
                                      {'deleted': False,
                                       'displayName': 'A Student',
                                       'emailAddress': 'student1@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'owner',
                                       'type': 'user'}],
                      'webViewLink': 'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'},
                     {'createdTime': '2020-09-16T20:24:10.734Z',
                      'name': 'Copy of Lab 9',
                      'owners': [{'displayName': 'A Student',
                                  'emailAddress': 'student2@stolaf.edu',
                                  'kind': 'drive#user',
                                  'me': False,
                                  'permissionId': '#####'}],
                      'permissions': [{'deleted': False,
                                       'displayName': 'ta-group',
                                       'emailAddress': 'ta-group@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'writer',
                                       'type': 'group'},
                                      {'deleted': False,
                                       'displayName': 'A Student',
                                       'emailAddress': 'student2@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'owner',
                                       'type': 'user'}],
                      'webViewLink': 'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'},
                     {'createdTime': '2020-09-16T15:54:59.679Z',
                      'name': 'Copy of Lab 8',
                      'owners': [{'displayName': 'A Student',
                                  'emailAddress': 'student3@stolaf.edu',
                                  'kind': 'drive#user',
                                  'me': False,
                                  'permissionId': '#####'}],
                      'permissions': [{'deleted': False,
                                       'displayName': 'ta-group',
                                       'emailAddress': 'ta-group@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'writer',
                                       'type': 'group'},
                                      {'deleted': False,
                                       'displayName': 'A Student',
                                       'emailAddress': 'student3@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'owner',
                                       'type': 'user'}],
                      'webViewLink': 'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk'}]

    assert token is None

    assert mock_service.q == ("modifiedTime > '2020-01-01T00:00:00' and "
                              "('an_email@stolaf.edu' in writers or 'an_email@stolaf.edu' in readers)")
    assert mock_service.pageToken is None


class MockServiceToken:

    # noinspection PyPep8Naming
    def __init__(self):
        self.q = ''
        self.pageSize = -1
        self.fields = ''
        self.pageToken = ''

    def files(self):
        return self

    # noinspection PyPep8Naming,PyUnusedLocal
    def list(self, q, pageSize, fields, pageToken):
        self.q = q

        self.pageToken = pageToken
        return self

    # noinspection PyMethodMayBeStatic
    def execute(self):
        return response_token


def test_request_files_with_token():
    mock_service = MockServiceToken()
    date = datetime.date(2020, 4, 12)
    files, token = request_files(mock_service, 'other-token', 'an_email@stolaf.edu', date)
    assert files == [{'createdTime': '2020-09-16T15:54:33.035Z',
                      'name': 'Copy of Lab 9',
                      'owners': [{'displayName': 'A Student',
                                  'emailAddress': 'student1@stolaf.edu',
                                  'kind': 'drive#user',
                                  'me': False,
                                  'permissionId': '#####'}],
                      'permissions': [{'deleted': False,
                                       'displayName': 'ta-group',
                                       'emailAddress': 'ta-group@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'writer',
                                       'type': 'group'},
                                      {'deleted': False,
                                       'displayName': 'A Student',
                                       'emailAddress': 'student1@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'owner',
                                       'type': 'user'}],
                      'webViewLink': 'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'},
                     {'createdTime': '2020-09-16T20:24:10.734Z',
                      'name': 'Copy of Lab 9',
                      'owners': [{'displayName': 'A Student',
                                  'emailAddress': 'student2@stolaf.edu',
                                  'kind': 'drive#user',
                                  'me': False,
                                  'permissionId': '#####'}],
                      'permissions': [{'deleted': False,
                                       'displayName': 'ta-group',
                                       'emailAddress': 'ta-group@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'writer',
                                       'type': 'group'},
                                      {'deleted': False,
                                       'displayName': 'A Student',
                                       'emailAddress': 'student2@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'owner',
                                       'type': 'user'}],
                      'webViewLink': 'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'},
                     {'createdTime': '2020-09-16T15:54:59.679Z',
                      'name': 'Copy of Lab 8',
                      'owners': [{'displayName': 'A Student',
                                  'emailAddress': 'student3@stolaf.edu',
                                  'kind': 'drive#user',
                                  'me': False,
                                  'permissionId': '#####'}],
                      'permissions': [{'deleted': False,
                                       'displayName': 'ta-group',
                                       'emailAddress': 'ta-group@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'writer',
                                       'type': 'group'},
                                      {'deleted': False,
                                       'displayName': 'A Student',
                                       'emailAddress': 'student3@stolaf.edu',
                                       'id': '#####',
                                       'kind': 'drive#permission',
                                       'role': 'owner',
                                       'type': 'user'}],
                      'webViewLink': 'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk'}]

    assert token == 'a-token'

    assert mock_service.q == ("modifiedTime > '2020-01-01T00:00:00' and "
                              "('an_email@stolaf.edu' in writers or 'an_email@stolaf.edu' in readers)")
    assert mock_service.pageToken == 'other-token'


def test_request_files_dates():
    for m in range(1, 7):
        mock_service = MockService()
        date = datetime.date(2020, m, 12)
        _, _ = request_files(mock_service, None, 'an_email@stolaf.edu', date)
        assert mock_service.q == ("modifiedTime > '2020-01-01T00:00:00' and "
                                  "('an_email@stolaf.edu' in writers or 'an_email@stolaf.edu' in readers)")

    for m in range(7, 13):
        mock_service = MockService()
        date = datetime.date(2020, m, 12)
        _, _ = request_files(mock_service, None, 'an_email@stolaf.edu', date)
        assert mock_service.q == ("modifiedTime > '2020-07-01T00:00:00' and "
                                  "('an_email@stolaf.edu' in writers or 'an_email@stolaf.edu' in readers)")


@mock.patch('stograde.drive.drive.request_files', return_value=(response['files'], None))
def test_get_all_files(mock_request):
    with mock.patch('stograde.drive.drive.build'):
        # noinspection PyTypeChecker
        files = get_all_files(None, 'ta-group@stolaf.edu')

    assert len(files) == 3
    assert files == {DriveResult('student1@stolaf.edu', 'Copy of Lab 9', '2020-09-16T15:54:33.035Z',
                                 'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'),
                     DriveResult('student2@stolaf.edu', 'Copy of Lab 9', '2020-09-16T20:24:10.734Z',
                                 'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'),
                     DriveResult('student3@stolaf.edu', 'Copy of Lab 8', '2020-09-16T15:54:59.679Z',
                                 'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk')}
    assert mock_request.call_count == 1


@mock.patch('stograde.drive.drive.request_files', side_effect=[(response['files'][0:2], 'a-token'),
                                                               (response['files'][2:], None)])
def test_get_all_files_multiple_pages(mock_request, capsys):
    with mock.patch('stograde.drive.drive.build'):
        # noinspection PyTypeChecker
        files = get_all_files(None, 'ta-group@stolaf.edu')

    assert len(files) == 3
    assert mock_request.call_count == 2
    out, _ = capsys.readouterr()
    assert out == '\r2 files processed\r3 files processed'


test_files_hw = [DriveResult('student1@stolaf.edu',
                             'Copy of HW 1 assignment',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'),
                 DriveResult('student2@stolaf.edu',
                             'Copy of HW1',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'),
                 DriveResult('student3@stolaf.edu',
                             'CopyOfHomeWork 001',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk'),
                 DriveResult('student4@stolaf.edu',
                             'Copy of HOMEWORK 000001',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_4/edit?usp=drivesdk'),
                 DriveResult('student5@stolaf.edu',
                             'CopyOfHomeWork1',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_5/edit?usp=drivesdk'),
                 DriveResult('student6@stolaf.edu',
                             'Copy of HOMEWORK 1',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_6/edit?usp=drivesdk'),
                 DriveResult('student7@stolaf.edu',
                             'aoisfgnoisdnfao',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_7/edit?usp=drivesdk'),
                 DriveResult('student8@stolaf.edu',
                             'lab3',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_8/edit?usp=drivesdk'),
                 DriveResult('student9@stolaf.edu',
                             'homework 11',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_9/edit?usp=drivesdk'),
                 ]

test_files_lab = [DriveResult('student1@stolaf.edu',
                              'Copy of LAB 1 assignment',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'),
                  DriveResult('student2@stolaf.edu',
                              'Copy of lab  1',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'),
                  DriveResult('student3@stolaf.edu',
                              'CopyOfLaB001',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk'),
                  DriveResult('student4@stolaf.edu',
                              'Copy of lab 01',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_4/edit?usp=drivesdk'),
                  DriveResult('student5@stolaf.edu',
                              'CopyOfLaB1',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_5/edit?usp=drivesdk'),
                  DriveResult('student6@stolaf.edu',
                              'Copy of HOMEWORK 1',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_6/edit?usp=drivesdk'),
                  DriveResult('student7@stolaf.edu',
                              'aoisfgnoisdnfao',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_7/edit?usp=drivesdk'),
                  DriveResult('student8@stolaf.edu',
                              'lab3',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_8/edit?usp=drivesdk'),
                  DriveResult('student9@stolaf.edu',
                              'lab 11',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_9/edit?usp=drivesdk'),
                  ]

test_files_ws = [DriveResult('student1@stolaf.edu',
                             'Copy of WS 1 assignment',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'),
                 DriveResult('student2@stolaf.edu',
                             'Copy of WS1',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'),
                 DriveResult('student3@stolaf.edu',
                             'Copy Of WorkSheet 01',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk'),
                 DriveResult('student4@stolaf.edu',
                             'CopyofWORKSHEET001',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_4/edit?usp=drivesdk'),
                 DriveResult('student5@stolaf.edu',
                             'Copy of WORKSHEET 1',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_5/edit?usp=drivesdk'),
                 DriveResult('student6@stolaf.edu',
                             'Copy of WORKSHEET 1',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_6/edit?usp=drivesdk'),
                 DriveResult('student7@stolaf.edu',
                             'aoisfgnoisdnfao',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_7/edit?usp=drivesdk'),
                 DriveResult('student8@stolaf.edu',
                             'lab3',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_8/edit?usp=drivesdk'),
                 DriveResult('student9@stolaf.edu',
                             'worksheet 11',
                             '2020-09-16T15:54:59.679Z',
                             'https://docs.google.com/document/d/the_document_id_9/edit?usp=drivesdk'),
                 ]

test_files_day = [DriveResult('student1@stolaf.edu',
                              'Copy of Day 1 assignment',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'),
                  DriveResult('student2@stolaf.edu',
                              'Copy of DAY1',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'),
                  DriveResult('student3@stolaf.edu',
                              'Copy Of Day 01',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk'),
                  DriveResult('student4@stolaf.edu',
                              'Copyof day 11',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_4/edit?usp=drivesdk'),
                  DriveResult('student5@stolaf.edu',
                              'Copy of WORKSHEET 1',
                              '2020-09-16T15:54:59.679Z',
                              'https://docs.google.com/document/d/the_document_id_5/edit?usp=drivesdk'),
                  ]


def test_get_assignment_files():
    with mock.patch('stograde.drive.drive.get_all_files', return_value=set(test_files_hw)):
        # noinspection PyTypeChecker
        files = get_assignment_files('hw1', None, '')
        assert files == set(test_files_hw[0:6])

    with mock.patch('stograde.drive.drive.get_all_files', return_value=test_files_lab):
        # noinspection PyTypeChecker
        files = get_assignment_files('lab1', None, '')
        assert files == set(test_files_lab[0:5])

    with mock.patch('stograde.drive.drive.get_all_files', return_value=test_files_ws):
        # noinspection PyTypeChecker
        files = get_assignment_files('ws1', None, '')
        assert files == set(test_files_ws[0:6])

    with mock.patch('stograde.drive.drive.get_all_files', return_value=test_files_day):
        # noinspection PyTypeChecker
        files = get_assignment_files('day1', None, '')
        assert files == set(test_files_day[0:3])


def test_get_assignment_files_parse_error(capsys):
    try:
        # noinspection PyTypeChecker
        get_assignment_files('gibberish4', None, '')
        raise AssertionError
    except SystemExit:
        pass

    _, err = capsys.readouterr()
    assert err == 'Could not parse assignment name gibberish4\n'


test_files_group = {DriveResult('student1@stolaf.edu',
                                'Copy of HW 1 assignment',
                                '2020-09-16T15:54:59.679Z',
                                'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'),
                    DriveResult('student2@stolaf.edu',
                                'Copy of HW1',
                                '2020-09-16T15:54:59.679Z',
                                'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'),
                    DriveResult('student3@stolaf.edu',
                                'CopyOfHomeWork1',
                                '2020-09-16T15:54:59.679Z',
                                'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk'),
                    DriveResult('student5@stolaf.edu',
                                'Copy hw1',
                                '2020-09-16T15:54:59.679Z',
                                'https://docs.google.com/document/d/the_document_id_5/edit?usp=drivesdk'),
                    DriveResult('student6@notstolaf.edu',
                                'Homework 1',
                                '2020-09-16T15:54:59.679Z',
                                'https://docs.google.com/document/d/the_document_id_6/edit?usp=drivesdk'),
                    DriveResult('student7@stolaf.edu',
                                'homework 1',
                                '2020-09-16T15:54:59.679Z',
                                'https://docs.google.com/document/d/the_document_id_7/edit?usp=drivesdk'),
                    DriveResult('student8@notstolaf.edu',
                                'Hw 1',
                                '2020-09-16T15:54:59.679Z',
                                'https://docs.google.com/document/d/the_document_id_8/edit?usp=drivesdk'),
                    DriveResult('student9@stolaf.edu',
                                'hw 1',
                                '2020-09-16T15:54:59.679Z',
                                'https://docs.google.com/document/d/the_document_id_9/edit?usp=drivesdk'),
                    }


def test_group_files():
    group1, group2, group3 = group_files(test_files_group, ['student1', 'student2', 'student3', 'student4', 'student5'])

    assert group1 == {DriveResult('student1@stolaf.edu',
                                  'Copy of HW 1 assignment',
                                  '2020-09-16T15:54:59.679Z',
                                  'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'),
                      DriveResult('student2@stolaf.edu',
                                  'Copy of HW1',
                                  '2020-09-16T15:54:59.679Z',
                                  'https://docs.google.com/document/d/the_document_id_2/edit?usp=drivesdk'),
                      DriveResult('student3@stolaf.edu',
                                  'CopyOfHomeWork1',
                                  '2020-09-16T15:54:59.679Z',
                                  'https://docs.google.com/document/d/the_document_id_3/edit?usp=drivesdk'),
                      DriveResult('student5@stolaf.edu',
                                  'Copy hw1',
                                  '2020-09-16T15:54:59.679Z',
                                  'https://docs.google.com/document/d/the_document_id_5/edit?usp=drivesdk'),
                      DriveResult('student4@stolaf.edu',
                                  'MISSING',
                                  None,
                                  'MISSING'),
                      }

    assert group2 == {DriveResult('student7@stolaf.edu',
                                  'homework 1',
                                  '2020-09-16T15:54:59.679Z',
                                  'https://docs.google.com/document/d/the_document_id_7/edit?usp=drivesdk'),
                      DriveResult('student9@stolaf.edu',
                                  'hw 1',
                                  '2020-09-16T15:54:59.679Z',
                                  'https://docs.google.com/document/d/the_document_id_9/edit?usp=drivesdk'),
                      }

    assert group3 == {DriveResult('student6@notstolaf.edu',
                                  'Homework 1',
                                  '2020-09-16T15:54:59.679Z',
                                  'https://docs.google.com/document/d/the_document_id_6/edit?usp=drivesdk'),
                      DriveResult('student8@notstolaf.edu',
                                  'Hw 1',
                                  '2020-09-16T15:54:59.679Z',
                                  'https://docs.google.com/document/d/the_document_id_8/edit?usp=drivesdk'),
                      }


def test_create_line():
    line = create_line(DriveResult('student1@stolaf.edu',
                                   'Copy of HW 1 assignment',
                                   '2020-09-16T15:54:59.679Z',
                                   'https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk'),
                       longest_email_len=21,
                       longest_file_name_len=25,
                       longest_link_len=75)

    assert line == ('student1@stolaf.edu   |'
                    ' Copy of HW 1 assignment   |'
                    ' https://docs.google.com/document/d/the_document_id_1/edit?usp=drivesdk      |'
                    ' 09/16/20 10:54:59 CDT')

    line = create_line(DriveResult('student1@stolaf.edu',
                                   'MISSING',
                                   None,
                                   'MISSING'),
                       longest_email_len=21,
                       longest_file_name_len=25,
                       longest_link_len=75)

    assert line == ('student1@stolaf.edu   |'
                    ' MISSING                   |'
                    ' MISSING                                                                     |'
                    ' ---------------------')


test_files_table = {DriveResult('student6@notstolaf.edu',
                                'Copy of HW 1 assignment',
                                '2020-09-16T15:54:59.679Z',
                                'the_document_url_6'),
                    DriveResult('a_student7@stolaf.edu',
                                'CopyOfHomeWork1',
                                '2020-09-03T17:44:07.241Z',
                                'the_document_url_7'),
                    DriveResult('zzz@notstolaf.edu',
                                'Hw 1',
                                '2020-08-26T16:13:12.745Z',
                                'a_url_8'),
                    DriveResult('student9@stolaf.edu',
                                'aoisfgnoisdnfaowersgsyhrteatgaerfgaerg',
                                '2019-12-06T00:39:12.818Z',
                                'the_document_url_9'),
                    DriveResult('student10@stolaf.edu',
                                'MISSING',
                                None,
                                'MISSING'),
                    }


def test_format_file_group():
    lines = format_file_group(test_files_table, 'A Title')

    assert '\n' + lines + '\n' == textwrap.dedent('''
    A Title
    EMAIL                  | FILE NAME                              | LINK               | CREATION DATE
    -----------------------+----------------------------------------+--------------------+----------------------
    a_student7@stolaf.edu  | CopyOfHomeWork1                        | the_document_url_7 | 09/03/20 12:44:07 CDT
    student10@stolaf.edu   | MISSING                                | MISSING            | ---------------------
    student6@notstolaf.edu | Copy of HW 1 assignment                | the_document_url_6 | 09/16/20 10:54:59 CDT
    student9@stolaf.edu    | aoisfgnoisdnfaowersgsyhrteatgaerfgaerg | the_document_url_9 | 12/05/19 18:39:12 CST
    zzz@notstolaf.edu      | Hw 1                                   | a_url_8            | 08/26/20 11:13:12 CDT
    ''')
