import shutil
import textwrap
import sys
import os

import pytest

from stograde.toolkit.__main__ import main
from stograde.toolkit.tabulate import asciiify

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'two_students_hw1', 'students', 'student2'))
def test_stograde_ci_passing(datafiles, capsys):
    os.chdir(str(datafiles))

    shutil.copytree(os.path.join(_dir, 'fixtures', 'two_students_hw1', 'data'), os.path.join(datafiles, 'data'))

    os.environ['CI_PROJECT_NAME'] = 'student2'
    os.environ['CI_PROJECT_NAMESPACE'] = 'sd/s20'

    argv = sys.argv
    sys.argv = [argv[0]] + ['ci', '--skip-spec-update', '--skip-version-check', '--skip-dependency-check']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == textwrap.dedent("\n"
                                  "USER      | 1 |  | \n"
                                  "----------+---+--+-\n"
                                  "student2  | 1 |  | \n\n")

    sys.argv = argv

    shutil.rmtree(os.path.join(datafiles, 'data'))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'two_students_hw1', 'students', 'rives'))
def test_stograde_ci_failing(datafiles, capsys, caplog):
    os.chdir(str(datafiles))

    shutil.copytree(os.path.join(_dir, 'fixtures', 'two_students_hw1', 'data'), os.path.join(datafiles, 'data'))

    os.environ['CI_PROJECT_NAME'] = 'rives'
    os.environ['CI_PROJECT_NAMESPACE'] = 'sd/s20'

    argv = sys.argv
    sys.argv = [argv[0]] + ['ci', '--skip-spec-update', '--skip-version-check', '--skip-dependency-check']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    log_messages = [log.msg for log in caplog.records]

    assert len(log_messages) == 4

    assert 'lab1: File Dog.h missing' in log_messages
    assert 'lab1: File Dog.cpp missing' in log_messages
    assert 'lab1: File Makefile missing' in log_messages
    assert 'lab1: File tryDog.cpp missing' in log_messages

    for log in caplog.records:
        assert log.levelname == 'ERROR'

    assert out == textwrap.dedent("\n"
                                  "USER   |  | 1 | \n"
                                  "-------+--+---+-\n"
                                  "rives  |  | - | \n\n")

    sys.argv = argv

    shutil.rmtree(os.path.join(datafiles, 'data'))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'two_students_hw1', 'students', 'student1'))
def test_stograde_ci_passing_stogradeignore(datafiles, capsys):
    os.chdir(str(datafiles))

    shutil.copytree(os.path.join(_dir, 'fixtures', 'two_students_hw1', 'data'), os.path.join(datafiles, 'data'))

    os.environ['CI_PROJECT_NAME'] = 'student1'
    os.environ['CI_PROJECT_NAMESPACE'] = 'sd/s20'

    argv = sys.argv
    sys.argv = [argv[0]] + ['ci', '--skip-spec-update', '--skip-version-check', '--skip-dependency-check']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == textwrap.dedent("\n"
                                  "USER      | 1 |  | \n"
                                  "----------+---+--+-\n"
                                  "student1  | 1 |  | \n\n")

    sys.argv = argv

    shutil.rmtree(os.path.join(datafiles, 'data'))
