import textwrap
import pytest
import locale
import sys
import os
import re
from io import StringIO
from cs251tk.cli.cs251tk import main


@pytest.fixture(scope='function', autouse=True)
def setup():
    # move the process into the test/ dir
    os.chdir("./test")

    # back up stdout/stderr and replace with testable version
    _stdout = sys.stdout
    _stderr = sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()

    # catch exceptions so that we always clean up
    try:
        yield sys.stdout, sys.stderr
    except Exception:
        pass

    # replace stdout/stderr with the actual versions
    sys.stdout.close()
    sys.stderr.close()
    sys.stdout = _stdout
    sys.stderr = _stderr

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

    assert regex.match(out)


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
