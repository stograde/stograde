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


@pytest.fixture(scope='function')
def setup(datafiles):
    # back up stdout/stderr and replace with testable version
    stdout = StringIO()
    stderr = StringIO()

    # catch exceptions so that we always clean up
    with redirect_stdout(stdout):
        with redirect_stderr(stderr):
            try:
                yield stdout, stderr
            except Exception:
                pass


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'two_students_hw1'))
def test_cs251tk_table(setup, datafiles):
    os.chdir(str(datafiles))

    stdout, stderr = setup
    sys.argv = [sys.argv[0]] + ['--no-update', '--no-check', '--skip-update-check']

    try:
        main()
    except SystemExit:
        pass

    out = stdout.getvalue()

    assert out == textwrap.dedent("""
    USER      | 1 | 1
    ----------+---+--
    rives     | - | -
    student2  | 1 | 1
    """)
