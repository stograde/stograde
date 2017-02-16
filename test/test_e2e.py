import sys
import os
import re
from textwrap import dedent
from cs251tk.cli.cs251tk import main


def test_cs251tk_version(capsys):
    sys.argv = [sys.argv[0]] + ['-v']
    os.chdir("test")

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    out = out.strip()
    regex = re.compile(r"version \d+[.]\d+[.]\d+")

    assert regex.match(out)

    os.chdir("..")


def test_cs251tk_table(capsys):
    sys.argv = [sys.argv[0]] + ['-n']
    os.chdir("test")

    main()

    out, err = capsys.readouterr()
    assert out == dedent("""
    USER      │ 1 │ 1
    ──────────┼───┼──
    [1mrives   [0m  │ ─ │ ─
    [1mstudent2[0m  │ 1 │ 1
    """)

    assert "[  ] rives, student2" in err
    assert "[· ] student2" in err
    assert "[··]" in err

    os.chdir("..")
