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
    sys.argv = [sys.argv[0]] + ['-v']

    try:
        main()
    except SystemExit:
        pass

    out = stdout.getvalue()
    out = out.strip()
    regex = re.compile(r"version \d+[.]\d+[.]\d+")

    assert regex.fullmatch(out)


def test_cs251tk_table(setup):
    stdout, stderr = setup
    sys.argv = [sys.argv[0]] + ['-n']

    try:
        main()
    except SystemExit:
        pass

    out = stdout.getvalue()
    err = stderr.getvalue()

    assert out == textwrap.dedent("""
    USER      │ 1 │ 1
    ──────────┼───┼──
    [1mrives   [0m  │ ─ │ ─
    [1mstudent2[0m  │ 1 │ 1
    """)

    assert "[  ] rives, student2" in err
    assert "[· ] student2" in err
    assert "[··]" in err
