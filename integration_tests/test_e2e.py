import textwrap
import pytest
import shutil
import sys
import os
import re
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from cs251tk.cli.cs251tk import main

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

    assert out == textwrap.dedent("""
    USER      | 1 | 1
    ----------+---+--
    rives     | - | -
    student2  | 1 | 1
    """)

    sys.argv = argv
