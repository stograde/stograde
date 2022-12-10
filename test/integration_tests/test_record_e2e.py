import re
import sys
import os
from unittest import mock

import pytest

from stograde.common import chdir
from stograde.toolkit.__main__ import main
from stograde.toolkit.subcommands import do_record
from test.utils import check_e2e_err_output

if os.getenv('SKIP_E2E') is not None:
    pytest.skip('Skipping Integration Tests', allow_module_level=True)

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_stograde_record(datafiles):
    args = [sys.argv[0]] + ['record', 'hw1', '--skip-repo-update', '--skip-spec-update', '--skip-version-check',
                            '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('sys.argv', args):
            main()

    assert (datafiles / 'logs' / 'log-hw1.md').isfile()


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_stograde_record_html(datafiles):
    args = [sys.argv[0]] + ['record', 'hw1', '--format', 'html', '--skip-repo-update', '--skip-spec-update',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        with mock.patch('sys.argv', args):
            main()

    assert (datafiles / 'logs' / 'log-hw1.html').isfile()


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_stograde_record_with_table(datafiles, capsys):
    args = [sys.argv[0]] + ['record', 'hw1', '--skip-repo-update', '--skip-spec-update', '--skip-version-check',
                            '--skip-dependency-check', '--table']

    with chdir(str(datafiles)):
        with mock.patch('sys.argv', args):
            main()

    out, err = capsys.readouterr()

    assert out == ("\n"
                   "USER      | 1 |  |  | \n"
                   "----------+---+--+--+-\n"
                   "rives     | - |  |  | \n"
                   "student1  | 1 |  |  | \n"
                   "student2  | 1 |  |  | \n"
                   "student3  | 1 |  |  | \n"
                   "student4  | 1 |  |  | \n"
                   "student5  | \x1b[1m\x1b[31m1\x1b[0m |  |  | \n\n")

    assert check_e2e_err_output(err)


@pytest.mark.skipif(os.getenv('GIST_TESTING_USER') is None or os.getenv('GIST_TESTING_USER') == '',
                    reason='Cannot run test without gist username')
@pytest.mark.skipif(os.getenv('GIST_TESTING_KEY') is None or os.getenv('GIST_TESTING_KEY') == '',
                    reason='Cannot run test without gist key')
@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_stograde_record_to_gist(datafiles, capsys):
    args = [sys.argv[0]] + ['record', 'hw1', '--skip-repo-update', '--skip-spec-update', '--skip-version-check',
                            '--skip-dependency-check', '--gist']

    with chdir(str(datafiles)):
        with mock.patch('sys.argv', args):
            with mock.patch('builtins.input', return_value=os.getenv('GIST_TESTING_USER')):
                with mock.patch('getpass.getpass', return_value=os.getenv('GIST_TESTING_KEY')):
                    main()

    out, err = capsys.readouterr()

    assert re.compile(r"^hw1 results are available at https://gist\.github\.com/.*\n$").match(out)

    assert check_e2e_err_output(err)


def test_do_record_bad_formatter():
    try:
        do_record([], [], '', '', 'main', {'clean': False, 'date': '', 'format': 'non-format'})
        raise AssertionError
    except ValueError:
        pass
