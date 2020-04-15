import textwrap
import sys
import os

import pytest

from stograde.common import chdir
from stograde.toolkit.__main__ import main

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_stograde_table(datafiles, capsys):
    argv = sys.argv
    sys.argv = [argv[0]] + ['table', '--skip-repo-update', '--skip-spec-update', '--skip-version-check',
                            '--skip-dependency-check']

    with chdir(str(datafiles)):
        try:
            main()
        except SystemExit:
            pass

    out, err = capsys.readouterr()
    print(bytes(out, 'utf-8'))

    assert out == textwrap.dedent("\n"
                                  "USER      | 1 | 1 | 1\n"
                                  "----------+---+---+--\n"
                                  "rives     | - | - | -\n"
                                  "student1  | 1 | - | -\n"
                                  "student2  | 1 | - | -\n"
                                  "student3  | 1 | - | -\n"
                                  "student4  | 1 | - | -\n"
                                  "student5  | \x1b[1m\x1b[31m1\x1b[0m | - | -\n\n")

    sys.argv = argv
