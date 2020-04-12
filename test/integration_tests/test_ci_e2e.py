import shutil
import textwrap
import sys
import os

import pytest

from stograde.toolkit import global_vars
from stograde.toolkit.__main__ import main

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'student2'))
def test_stograde_ci_passing(datafiles, capsys):
    os.chdir(str(datafiles))

    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

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
    global_vars.CI = False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'student1'))
def test_stograde_ci_passing_stogradeignore_some_assignments(datafiles, capsys, caplog):
    os.chdir(str(datafiles))

    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

    os.environ['CI_PROJECT_NAME'] = 'student1'
    os.environ['CI_PROJECT_NAMESPACE'] = 'sd/s20'

    argv = sys.argv
    sys.argv = [argv[0]] + ['ci', '--skip-spec-update', '--skip-version-check', '--skip-dependency-check']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    log_messages = [log.msg for log in caplog.records]

    assert len(log_messages) == 1

    assert log_messages[0] == 'Skipping lab1: ignored by stogradeignore'

    for log in caplog.records:
        assert log.levelname == 'WARNING'

    assert out == textwrap.dedent("\n"
                                  "USER      | 1 |  | \n"
                                  "----------+---+--+-\n"
                                  "student1  | 1 |  | \n\n")

    sys.argv = argv

    shutil.rmtree(os.path.join(datafiles, 'data'))
    global_vars.CI = False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'narvae1'))
def test_stograde_ci_passing_stogradeignore_all_assignments(datafiles, capsys, caplog):
    os.chdir(str(datafiles))

    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

    os.environ['CI_PROJECT_NAME'] = 'narvae1'
    os.environ['CI_PROJECT_NAMESPACE'] = 'sd/s20'

    argv = sys.argv
    sys.argv = [argv[0]] + ['ci', '--skip-spec-update', '--skip-version-check', '--skip-dependency-check']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    log_messages = [log.msg for log in caplog.records]

    assert len(log_messages) == 3

    assert 'Skipping hw1: ignored by stogradeignore' in log_messages
    assert 'Skipping lab1: ignored by stogradeignore' in log_messages
    assert 'All assignments ignored by stogradeignore' in log_messages

    for log in caplog.records:
        assert log.levelname == 'WARNING'

    assert out == textwrap.dedent('No specs loaded!\n')

    sys.argv = argv

    shutil.rmtree(os.path.join(datafiles, 'data'))
    global_vars.CI = False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'student4'))
def test_stograde_ci_passing_with_optional_compile(datafiles, capsys, caplog):
    os.chdir(str(datafiles))

    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

    os.environ['CI_PROJECT_NAME'] = 'student4'
    os.environ['CI_PROJECT_NAMESPACE'] = 'sd/s20'

    argv = sys.argv
    sys.argv = [argv[0]] + ['ci', '--skip-spec-update', '--skip-version-check', '--skip-dependency-check']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    log_messages = [log.msg for log in caplog.records]

    assert len(log_messages) == 1

    assert log_messages[0] == 'hw1: File secondComment.cpp compile error (This did not fail the build)'

    for log in caplog.records:
        assert log.levelname == 'WARNING'

    assert out == textwrap.dedent("\n"
                                  "USER      | 1 |  | \n"
                                  "----------+---+--+-\n"
                                  "student4  | 1 |  | \n\n")

    sys.argv = argv

    shutil.rmtree(os.path.join(datafiles, 'data'))
    global_vars.CI = False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'rives'))
def test_stograde_ci_failing(datafiles, capsys, caplog):
    os.chdir(str(datafiles))

    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

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
    global_vars.CI = False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'students', 'student3'))
def test_stograde_ci_failing_compile(datafiles, capsys, caplog):
    os.chdir(str(datafiles))

    shutil.copytree(os.path.join(_dir, 'fixtures', 'data'), os.path.join(datafiles, 'data'))

    os.environ['CI_PROJECT_NAME'] = 'student3'
    os.environ['CI_PROJECT_NAMESPACE'] = 'sd/s20'

    argv = sys.argv
    sys.argv = [argv[0]] + ['ci', '--skip-spec-update', '--skip-version-check', '--skip-dependency-check']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    log_messages = [log.msg for log in caplog.records]

    assert len(log_messages) == 1

    assert log_messages[0] == "hw1: File hello.cpp compile error:\n\n\t" \
                              "./hello.cpp: In function ‘int main()’:\n\t" \
                              "./hello.cpp:11:12: error: expected ‘}’ at end of input\n\t" \
                              "    return 0;\n\t" \
                              "            ^\n\t"

    for log in caplog.records:
        assert log.levelname == 'ERROR'

    assert out == textwrap.dedent("\n"
                                  "USER      | 1 |  | \n"
                                  "----------+---+--+-\n"
                                  "student3  | 1 |  | \n\n")

    sys.argv = argv

    shutil.rmtree(os.path.join(datafiles, 'data'))
    global_vars.CI = False
