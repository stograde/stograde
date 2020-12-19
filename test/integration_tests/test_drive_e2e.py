import os
import sys
import textwrap
from unittest import mock

import pytest

from stograde.common import chdir
from stograde.drive.drive_result import DriveResult
from stograde.toolkit.__main__ import main

if os.getenv('SKIP_E2E') is not None:
    pytest.skip('Skipping Integration Tests', allow_module_level=True)

_dir = os.path.dirname(os.path.realpath(__file__))

test_files = {DriveResult('student1@stolaf.edu',
                          'Copy of HW 1 assignment',
                          '2020-08-26T14:23:49.149Z',
                          'the_document_url_1'),
              DriveResult('student2@stolaf.edu',
                          'Copy of HW1',
                          '2019-12-06T00:39:12.818Z',
                          'a_url'),
              DriveResult('student3@stolaf.edu',
                          'CopyOfHomeWork1',
                          '2020-09-16T15:54:59.679Z',
                          '3rd_url'),
              DriveResult('student5@stolaf.edu',
                          'Copy hw1',
                          '2020-09-03T17:44:07.241Z',
                          'doc_url_4'),
              DriveResult('student6@notstolaf.edu',
                          'Homework 1',
                          '2020-05-26T00:37:18.256Z',
                          'document_5_url'),
              DriveResult('student7@stolaf.edu',
                          'homework 1',
                          '2020-02-08T06:33:06.941Z',
                          'doc_6'),
              DriveResult('student8@notstolaf.edu',
                          'Hw 1',
                          '2020-01-05T20:40:26.571Z',
                          'url_7'),
              DriveResult('student9@stolaf.edu',
                          'hw 1',
                          '2020-11-13T22:34:47.255Z',
                          'a_longer_url_for_document_8'),
              }


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_stograde_drive(datafiles, capsys):
    args = [sys.argv[0]] + ['drive', 'hw1', '--skip-version-check', '--skip-dependency-check',
                            '-e', 'an_email@email.com']
    with chdir(str(datafiles)):
        with mock.patch('stograde.toolkit.subcommands.get_assignment_files', return_value=test_files):
            with mock.patch('stograde.toolkit.subcommands.authenticate_drive'):
                with mock.patch('sys.argv', args):
                    main()

    out, _ = capsys.readouterr()
    assert out == textwrap.dedent('''

    Files shared from students in class:
    EMAIL               | FILE NAME               | LINK               | CREATION DATE
    --------------------+-------------------------+--------------------+----------------------
    rives@stolaf.edu    | MISSING                 | MISSING            | ---------------------
    student1@stolaf.edu | Copy of HW 1 assignment | the_document_url_1 | 08/26/20 09:23:49 CDT
    student2@stolaf.edu | Copy of HW1             | a_url              | 12/05/19 18:39:12 CST
    student3@stolaf.edu | CopyOfHomeWork1         | 3rd_url            | 09/16/20 10:54:59 CDT
    student4@stolaf.edu | MISSING                 | MISSING            | ---------------------
    student5@stolaf.edu | Copy hw1                | doc_url_4          | 09/03/20 12:44:07 CDT

    Files shared from students NOT in class:
    EMAIL               | FILE NAME  | LINK                        | CREATION DATE
    --------------------+------------+-----------------------------+----------------------
    student7@stolaf.edu | homework 1 | doc_6                       | 02/08/20 00:33:06 CST
    student9@stolaf.edu | hw 1       | a_longer_url_for_document_8 | 11/13/20 16:34:47 CST

    Files shared from personal emails:
    EMAIL                  | FILE NAME  | LINK           | CREATION DATE
    -----------------------+------------+----------------+----------------------
    student6@notstolaf.edu | Homework 1 | document_5_url | 05/25/20 19:37:18 CDT
    student8@notstolaf.edu | Hw 1       | url_7          | 01/05/20 14:40:26 CST
    ''')


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_stograde_drive_no_files(datafiles, capsys):
    args = [sys.argv[0]] + ['drive', 'hw1', '--skip-version-check', '--skip-dependency-check',
                            '-e', 'an_email@email.com']
    with chdir(str(datafiles)):
        with mock.patch('stograde.toolkit.subcommands.get_assignment_files', return_value=set()):
            with mock.patch('stograde.toolkit.subcommands.authenticate_drive'):
                with mock.patch('sys.argv', args):
                    try:
                        main()
                        raise AssertionError
                    except SystemExit:
                        pass

    _, err = capsys.readouterr()
    assert err == '\nNo files found!\n'
