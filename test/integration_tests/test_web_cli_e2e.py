import os
import sys
from unittest import mock

import pytest

from stograde.common import chdir
from stograde.toolkit.__main__ import main
from stograde.webapp import server

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'web_tests'))
def test_stograde_web_student_menu(datafiles, capsys):
    args = [sys.argv[0]] + ['web', '--port', '1500', 'hw2',
                            '--skip-repo-update', '--skip-spec-update',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('stograde.webapp.web_cli.prompt') as mock_prompt:
            with mock.patch('sys.argv', args):
                mock_prompt.side_effect = []
                try:
                    main()
                    raise AssertionError
                except StopIteration:
                    pass
                assert mock_prompt.call_args[0][0][0] == {
                    'type': 'list',
                    'name': 'student',
                    'message': 'Choose student',
                    'choices': ['QUIT', 'student6', 'student7 NO SUBMISSION', 'student8'],
                }
                assert mock_prompt.call_count == 1

    out, _ = capsys.readouterr()

    assert out == 'Loading repos. Please wait...\n'


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'web_tests'))
def test_stograde_web_student_menu_blank(datafiles, capsys):
    args = [sys.argv[0]] + ['web', '--port', '1501', 'hw2',
                            '--skip-repo-update', '--skip-spec-update',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('stograde.webapp.web_cli.prompt') as mock_prompt:
            with mock.patch('sys.argv', args):
                mock_prompt.side_effect = [None]
                main()
                assert mock_prompt.call_count == 1

    out, _ = capsys.readouterr()

    assert out == 'Loading repos. Please wait...\n'


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'web_tests'))
def test_stograde_web_student_menu_quit(datafiles, capsys):
    args = [sys.argv[0]] + ['web', '--port', '1502', 'hw2',
                            '--skip-repo-update', '--skip-spec-update',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('stograde.webapp.web_cli.prompt') as mock_prompt:
            with mock.patch('sys.argv', args):
                mock_prompt.side_effect = [{'student': 'QUIT'}]
                main()
                assert mock_prompt.call_count == 1

    out, _ = capsys.readouterr()

    assert out == 'Loading repos. Please wait...\n'


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'web_tests'))
def test_stograde_web_student_menu_student_no_submission(datafiles, capsys):
    args = [sys.argv[0]] + ['web', '--port', '1503', 'hw2',
                            '--skip-repo-update', '--skip-spec-update',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('stograde.webapp.web_cli.prompt') as mock_prompt:
            with mock.patch('sys.argv', args):
                mock_prompt.side_effect = [{'student': 'student7 NO SUBMISSION'}]
                try:
                    main()
                    raise AssertionError
                except StopIteration:
                    pass
                assert mock_prompt.call_args[0][0][0] == {
                    'type': 'list',
                    'name': 'student',
                    'message': 'Choose student',
                    'choices': ['QUIT', 'student6', 'student7 NO SUBMISSION', 'student8'],
                }
                assert mock_prompt.call_count == 2

    out, _ = capsys.readouterr()

    assert out == 'Loading repos. Please wait...\n'


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'web_tests'))
def test_stograde_web_file_menu(datafiles, capsys):
    args = [sys.argv[0]] + ['web', '--port', '1504', 'hw2',
                            '--skip-repo-update', '--skip-spec-update',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('stograde.webapp.web_cli.prompt') as mock_prompt:
            with mock.patch('sys.argv', args):
                mock_prompt.side_effect = [{'student': 'student6'}]
                try:
                    main()
                    raise AssertionError
                except StopIteration:
                    pass

                assert mock_prompt.call_args[0][0][0] == {
                    'type': 'list',
                    'name': 'file',
                    'message': 'Choose file',
                    'choices': ['BACK', 'second.cpp', 'third.cpp'],
                }
                assert mock_prompt.call_count == 2

    out, _ = capsys.readouterr()

    assert out == 'Loading repos. Please wait...\nProcessing...\n'


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'web_tests'))
def test_stograde_web_file_menu_missing_files(datafiles, capsys):
    args = [sys.argv[0]] + ['web', '--port', '1505', 'hw2',
                            '--skip-repo-update', '--skip-spec-update',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('stograde.webapp.web_cli.prompt') as mock_prompt:
            with mock.patch('sys.argv', args):
                mock_prompt.side_effect = [{'student': 'student8'}]
                try:
                    main()
                    raise AssertionError
                except StopIteration:
                    pass

                assert mock_prompt.call_args[0][0][0] == {
                    'type': 'list',
                    'name': 'file',
                    'message': 'Choose file',
                    'choices': ['BACK', 'second.cpp MISSING', 'third.cpp MISSING (OPTIONAL)'],
                }
                assert mock_prompt.call_count == 2

    out, _ = capsys.readouterr()

    assert out == 'Loading repos. Please wait...\nProcessing...\n'


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'web_tests'))
def test_stograde_web_file_menu_back(datafiles, capsys):
    args = [sys.argv[0]] + ['web', '--port', '1506', 'hw2',
                            '--skip-repo-update', '--skip-spec-update',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('stograde.webapp.web_cli.prompt') as mock_prompt:
            with mock.patch('sys.argv', args):
                mock_prompt.side_effect = [{'student': 'student6'},
                                           {'file': 'BACK'}]
                try:
                    main()
                    raise AssertionError
                except StopIteration:
                    pass

                assert mock_prompt.call_args[0][0][0] == {
                    'type': 'list',
                    'name': 'student',
                    'message': 'Choose student',
                    'choices': ['QUIT', 'student6', 'student7 NO SUBMISSION', 'student8'],
                }
                assert mock_prompt.call_count == 3

    out, _ = capsys.readouterr()

    assert out == 'Loading repos. Please wait...\nProcessing...\n'


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'web_tests'))
def test_stograde_web_file_menu_blank(datafiles, capsys):
    args = [sys.argv[0]] + ['web', '--port', '1507', 'hw2',
                            '--skip-repo-update', '--skip-spec-update',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('stograde.webapp.web_cli.prompt') as mock_prompt:
            with mock.patch('sys.argv', args):
                mock_prompt.side_effect = [{'student': 'student6'},
                                           None]
                try:
                    main()
                    raise AssertionError
                except StopIteration:
                    pass

                assert mock_prompt.call_args[0][0][0] == {
                    'type': 'list',
                    'name': 'student',
                    'message': 'Choose student',
                    'choices': ['QUIT', 'student6', 'student7 NO SUBMISSION', 'student8'],
                }
                assert mock_prompt.call_count == 3

    out, _ = capsys.readouterr()

    assert out == 'Loading repos. Please wait...\nProcessing...\n'


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'web_tests'))
def test_stograde_web_file_menu_file(datafiles, capsys):
    args = [sys.argv[0]] + ['web', '--port', '1508', 'hw2',
                            '--skip-repo-update', '--skip-spec-update',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('stograde.webapp.web_cli.prompt') as mock_prompt:
            with mock.patch('sys.argv', args):
                mock_prompt.side_effect = [{'student': 'student6'},
                                           {'file': 'second.cpp'}]

                assert server.work_dir == '.'

                try:
                    main()
                    raise AssertionError
                except StopIteration:
                    pass

                assert mock_prompt.call_args[0][0][0] == {
                    'type': 'list',
                    'name': 'file',
                    'message': 'Choose file',
                    'choices': ['BACK', 'second.cpp', 'third.cpp'],
                }
                assert mock_prompt.call_count == 3

                assert server.work_dir != '.'

    out, _ = capsys.readouterr()

    assert out == 'Loading repos. Please wait...\nProcessing...\n'
