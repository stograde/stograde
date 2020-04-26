import os
import sys
from unittest import mock

import pytest

from stograde.common import version, chdir
from stograde.toolkit import global_vars
from stograde.toolkit.__main__ import main
from stograde.toolkit.args import process_args

_dir = os.path.dirname(os.path.realpath(__file__))


def test_version_flag(capsys):
    try:
        with mock.patch('sys.argv', [sys.argv[0], '--version']):
            main()
    except SystemExit:
        pass

    out, _ = capsys.readouterr()

    assert out == 'version {}\n'.format(version)

    try:
        with mock.patch('sys.argv', [sys.argv[0], '-v']):
            main()
    except SystemExit:
        pass

    out, _ = capsys.readouterr()

    assert out == 'version {}\n'.format(version)


@mock.patch.dict(os.environ, {'CI_PROJECT_NAME': 'student7', 'CI_PROJECT_NAMESPACE': 'sd/s20'})
@mock.patch('sys.argv', [sys.argv[0], 'ci'])
@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'student7'))
def test_process_args_ci(datafiles):
    with chdir(str(datafiles)):
        args, students, assignments = process_args()

    assert students == ['student7']
    assert set(assignments) == {'hw4', 'hw7', 'lab4', 'ws2'}
    assert args['course'] == 'sd/s20'
    assert global_vars.CI is True

    global_vars.CI = False


def test_process_args_record_one_assignment():
    args = [sys.argv[0]] + ['record', 'hw5', '--student', 'student6']

    with mock.patch('sys.argv', args):
        _, students, assignments = process_args()

    assert students == ['student6']
    assert assignments == ['hw5']


def test_process_args_record_multiple_assignments():
    args = [sys.argv[0]] + ['record', 'hw5', 'lab3', 'hw13', '--student', 'student8']

    with mock.patch('sys.argv', args):
        _, students, assignments = process_args()

    assert students == ['student8']
    assert set(assignments) == {'hw5', 'lab3', 'hw13'}


def test_process_args_table():
    args = [sys.argv[0]] + ['table', '--student', 'student10']

    with mock.patch('sys.argv', args):
        _, students, assignments = process_args()

    assert students == ['student10']
    assert not assignments


def test_process_args_web():
    args = [sys.argv[0]] + ['web', 'hw1', '--student', 'student12', '--port', '12345']

    with mock.patch('sys.argv', args):
        _, students, assignments = process_args()

    assert students == ['student12']
    assert assignments == ['hw1']


def test_process_args_repo():
    args = [sys.argv[0]] + ['repo', 'clone', '--student', 'student9']

    with mock.patch('sys.argv', args):
        _, students, assignments = process_args()

    assert students == ['student9']
    assert not assignments


def test_no_sub_command(capsys):
    try:
        with mock.patch('sys.argv', [sys.argv[0]]):
            main()
    except SystemExit:
        pass

    _, err = capsys.readouterr()

    assert err == 'Sub-command must be specified\n'


def test_no_students(tmpdir, capsys):
    args = [sys.argv[0]] + ['record', 'hw1']

    with tmpdir.as_cwd():
        try:
            with mock.patch('sys.argv', args):
                main()
        except SystemExit:
            pass

    _, err = capsys.readouterr()

    assert err == 'No students selected\nIs your students.txt missing?\n'
