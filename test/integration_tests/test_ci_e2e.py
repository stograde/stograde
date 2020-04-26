import shutil
import sys
import os
from unittest import mock

import pytest

from stograde.common import chdir
from stograde.toolkit.__main__ import main

_dir = os.path.dirname(os.path.realpath(__file__))
ci_args = [sys.argv[0]] + ['ci', '--skip-spec-update', '--skip-version-check', '--skip-dependency-check']


pytest.skip('testing coverage without integration tests', allow_module_level=True)


@mock.patch.dict(os.environ, {'CI_PROJECT_NAME': 'student2', 'CI_PROJECT_NAMESPACE': 'sd/s20'})
@mock.patch('sys.argv', ci_args)
@mock.patch('stograde.toolkit.global_vars.CI', True)
@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'student2'))
def test_stograde_ci_passing(datafiles, capsys):
    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

    with chdir(str(datafiles)):
        try:
            main()
        except SystemExit:
            pass

    out, _ = capsys.readouterr()

    assert out == ("\n"
                   "USER      | 1 |  | \n"
                   "----------+---+--+-\n"
                   "student2  | 1 |  | \n\n")


@mock.patch.dict(os.environ, {'CI_PROJECT_NAME': 'student1', 'CI_PROJECT_NAMESPACE': 'sd/s20'})
@mock.patch('sys.argv', ci_args)
@mock.patch('stograde.toolkit.global_vars.CI', True)
@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'student1'))
def test_stograde_ci_passing_stogradeignore_some_assignments(datafiles, capsys, caplog):
    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

    with chdir(str(datafiles)):
        try:
            main()
        except SystemExit:
            pass

    out, _ = capsys.readouterr()

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('Skipping lab1: ignored by stogradeignore', 'WARNING')}

    assert out == ("\n"
                   "USER      | 1 |  | \n"
                   "----------+---+--+-\n"
                   "student1  | 1 |  | \n\n")


@mock.patch.dict(os.environ, {'CI_PROJECT_NAME': 'narvae1', 'CI_PROJECT_NAMESPACE': 'sd/s20'})
@mock.patch('sys.argv', ci_args)
@mock.patch('stograde.toolkit.global_vars.CI', True)
@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'narvae1'))
def test_stograde_ci_passing_stogradeignore_all_assignments(datafiles, capsys, caplog):
    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

    with chdir(str(datafiles)):
        try:
            main()
        except SystemExit:
            pass

    out, _ = capsys.readouterr()

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('Skipping hw1: ignored by stogradeignore', 'WARNING'),
                            ('Skipping lab1: ignored by stogradeignore', 'WARNING'),
                            ('All assignments ignored by stogradeignore', 'WARNING')}

    assert out == 'No specs loaded!\n'


@mock.patch.dict(os.environ, {'CI_PROJECT_NAME': 'student4', 'CI_PROJECT_NAMESPACE': 'sd/s20'})
@mock.patch('sys.argv', ci_args)
@mock.patch('stograde.toolkit.global_vars.CI', True)
@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'student4'))
def test_stograde_ci_passing_with_optional_compile(datafiles, capsys, caplog):
    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

    with chdir(str(datafiles)):
        try:
            main()
        except SystemExit:
            pass

    out, _ = capsys.readouterr()

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('hw1: File secondComment.cpp compile error (This did not fail the build)', 'WARNING')}

    assert out == ("\n"
                   "USER      | 1 |  | \n"
                   "----------+---+--+-\n"
                   "student4  | 1 |  | \n\n")


@mock.patch.dict(os.environ, {'CI_PROJECT_NAME': 'rives', 'CI_PROJECT_NAMESPACE': 'sd/s20'})
@mock.patch('sys.argv', ci_args)
@mock.patch('stograde.toolkit.global_vars.CI', True)
@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'rives'))
def test_stograde_ci_failing(datafiles, capsys, caplog):
    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

    with chdir(str(datafiles)):
        try:
            main()
        except SystemExit:
            pass

    out, _ = capsys.readouterr()

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('lab1: File Dog.h missing', 'ERROR'),
                            ('lab1: File Dog.cpp missing', 'ERROR'),
                            ('lab1: File Makefile missing', 'ERROR'),
                            ('lab1: File tryDog.cpp missing', 'ERROR')}

    assert out == ("\n"
                   "USER   |  | 1 | \n"
                   "-------+--+---+-\n"
                   "rives  |  | - | \n\n")


@mock.patch.dict(os.environ, {'CI_PROJECT_NAME': 'student3', 'CI_PROJECT_NAMESPACE': 'sd/s20'})
@mock.patch('sys.argv', ci_args)
@mock.patch('stograde.toolkit.global_vars.CI', True)
@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'student3'))
def test_stograde_ci_failing_compile(datafiles, capsys, caplog):
    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

    with chdir(str(datafiles)):
        try:
            main()
        except SystemExit:
            pass

    out, _ = capsys.readouterr()

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {("hw1: File hello.cpp compile error:\n\n\t"
                             "./hello.cpp: In function ‘int main()’:\n\t"
                             "./hello.cpp:11:12: error: expected ‘}’ at end of input\n\t"
                             "    return 0;\n\t"
                             "            ^\n\t", 'ERROR')}

    assert out == ("\n"
                   "USER      | 1 |  | \n"
                   "----------+---+--+-\n"
                   "student3  | 1 |  | \n\n")
