import textwrap
import pytest
import locale
import sys
import os
import re
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from cs251tk.cli.cs251tk import main


@pytest.fixture(scope='function', autouse=True)
def setup():
    # move the process into the test/ dir
    os.chdir("./test")

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

    # return to the previous directory
    os.chdir("..")


def test_cs251tk_version(setup):
    stdout, stderr = setup
    sys.argv = [sys.argv[0]] + ['-v', '--skip-update-check']

    try:
        main()
    except SystemExit:
        pass

    out = stdout.getvalue()

    assert out.startswith("version ")


def test_cs251tk_table(setup):
    stdout, stderr = setup
    sys.argv = [sys.argv[0]] + ['--no-update', '--no-check', '--skip-update-check']

    try:
        main()
    except SystemExit:
        pass

    out = stdout.getvalue()

    assert out == textwrap.dedent("""
    USER      │ 1 │ 1
    ──────────┼───┼──
    rives     │ ─ │ ─
    student2  │ 1 │ 1
    """)
