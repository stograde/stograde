import os

import pytest

from stograde.common import chdir
from stograde.process_assignment import import_supporting, remove_supporting
from stograde.specs.spec import Spec
from stograde.specs.supporting_file import SupportingFile
from test.common.test_find_unmerged_branches_in_cwd import touch

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'supporting'))
def test_import_supporting(datafiles, tmpdir):
    spec = Spec('hw1', 'hw1', None,
                supporting_files=[SupportingFile('a_file.txt', 'a_file.txt'),
                                  SupportingFile('another_file.txt', '../another_file.txt')])

    with tmpdir.as_cwd():
        os.makedirs('subdir')
        with chdir('subdir'):
            supporting_dir, written_files = import_supporting(spec=spec, basedir=str(datafiles))

            assert os.path.exists('a_file.txt')
            assert os.path.exists('../another_file.txt')

    assert supporting_dir == os.path.join(datafiles, 'data', 'supporting')
    assert written_files == ['a_file.txt', '../another_file.txt']


def test_remove_supporting(tmpdir):
    with tmpdir.as_cwd():
        os.makedirs('subdir')
        with chdir('subdir'):
            touch('file1.txt')
            touch('../file2.txt')

            assert os.path.exists('file1.txt')
            assert os.path.exists('../file2.txt')
            assert not os.path.exists('file3.txt')

            remove_supporting(['file1.txt', '../file2.txt', 'file3.txt'])

            assert not os.path.exists('file1.txt')
            assert not os.path.exists('../file2.txt')
            assert not os.path.exists('file3.txt')
