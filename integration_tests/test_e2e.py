import textwrap
import sys
import os

import pytest

from cs251tk.toolkit.__main__ import main

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'two_students_hw1'))
def test_cs251tk_table(datafiles, capsys):
    os.chdir(str(datafiles))

    argv = sys.argv
    sys.argv = [argv[0]] + ['--no-update', '--no-check', '--skip-update-check']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == textwrap.dedent("USER      | 1 | 1 | 1\n"
                                  "----------+---+---+--\n"
                                  "rives     | - | - | -\n"
                                  "student2  | 1 | 1 | -\n")

    sys.argv = argv


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'two_students_hw1'))
def test_cs251tk_hidden_table(datafiles, capsys):
    os.chdir(str(datafiles))

    argv = sys.argv
    sys.argv = [argv[0]] + ['--no-update', '--no-check', '--skip-update-check', '--quiet']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == ""

    sys.argv = argv


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'two_students_hw1'))
def test_cs251tk_record(datafiles, capsys):
    os.chdir(str(datafiles))

    argv = sys.argv
    sys.argv = [argv[0]] + ['--record=hw1', '--no-update', '--no-check', '--skip-update-check']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == textwrap.dedent("USER      | 1 | 1 | 1\n"
                                  "----------+---+---+--\n"
                                  "rives     | - | - | -\n"
                                  "student2  | 1 | 1 | -\n")

    assert (datafiles / 'logs' / 'log-hw1.md').isfile()

    sys.argv = argv
