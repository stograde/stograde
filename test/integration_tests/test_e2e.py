import textwrap
import sys
import os

import pytest

from stograde.toolkit.__main__ import main

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'two_students_hw1'))
def test_stograde_table(datafiles, capsys):
    os.chdir(str(datafiles))

    argv = sys.argv
    sys.argv = [argv[0]] + ['table', '--skip-repo-update', '--skip-spec-update', '--skip-version-check',
                            '--skip-known-host-check', '--no-partials']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == textwrap.dedent("\n"
                                  "USER      | 1 | 1 | 1\n"
                                  "----------+---+---+--\n"
                                  "rives     | - | - | -\n"
                                  "student2  | 1 | 1 | -\n\n")

    sys.argv = argv


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'two_students_hw1'))
def test_stograde_hidden_table(datafiles, capsys):
    os.chdir(str(datafiles))

    argv = sys.argv
    sys.argv = [argv[0]] + ['record', 'hw1', '--skip-repo-update', '--skip-spec-update', '--skip-version-check',
                            '--skip-known-host-check']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == ""

    sys.argv = argv


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'two_students_hw1'))
def test_stograde_record(datafiles):
    os.chdir(str(datafiles))

    argv = sys.argv
    sys.argv = [argv[0]] + ['record', 'hw1', '--skip-repo-update', '--skip-spec-update', '--skip-version-check',
                            '--skip-known-host-check']

    try:
        main()
    except SystemExit:
        pass

    assert (datafiles / 'logs' / 'log-hw1.md').isfile()

    sys.argv = argv
