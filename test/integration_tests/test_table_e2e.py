import textwrap
import sys
import os

import pytest

from stograde.toolkit.__main__ import main

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_stograde_table(datafiles, capsys):
    os.chdir(str(datafiles))

    argv = sys.argv
    sys.argv = [argv[0]] + ['table', '--skip-repo-update', '--skip-spec-update', '--skip-version-check',
                            '--skip-dependency-check', '--no-partials']

    try:
        main()
    except SystemExit:
        pass

    out, err = capsys.readouterr()
    print(out)

    assert out == textwrap.dedent("\n"
                                  "USER      | 1 | 1 | 1\n"
                                  "----------+---+---+--\n"
                                  "rives     | - | - | -\n"
                                  "student2  | 1 | 1 | -\n\n")

    sys.argv = argv
