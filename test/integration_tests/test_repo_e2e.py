import os
import sys
from unittest import mock

import pytest

from stograde.common import chdir
from stograde.student import clone_url
from stograde.toolkit.__main__ import main
from test.utils import touch

if os.getenv('SKIP_E2E') is not None:
    pytest.skip('Skipping Integration Tests', allow_module_level=True)

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'repo_tests'))
def test_repo_clone(datafiles):
    student_path = os.path.join(datafiles, 'students', 'cs251-specs')

    args = [sys.argv[0]] + ['repo', 'clone', '--stogit', 'https://github.com/StoDevX', '--course', 'sd',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        assert not os.path.exists(student_path)

        with mock.patch('sys.argv', args):
            main()

        assert os.path.exists(student_path)


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'repo_tests'))
def test_repo_update(datafiles):
    student_path = os.path.join(datafiles, 'students', 'cs251-specs')

    args = [sys.argv[0]] + ['repo', 'update', '--stogit', 'https://github.com/StoDevX', '--course', 'sd',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        assert not os.path.exists(student_path)

        with mock.patch('sys.argv', args):
            main()

        assert os.path.exists(student_path)


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'repo_tests'))
def test_repo_clean(datafiles):
    student_path = os.path.join(datafiles, 'students', 'cs251-specs')

    args = [sys.argv[0]] + ['repo', 'clean', '--stogit', 'https://github.com/StoDevX', '--course', 'sd',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        assert not os.path.exists(student_path)
        clone_url('https://github.com/StoDevX/cs251-specs', student_path)
        touch(os.path.join(student_path, 'a_file'))
        assert os.path.exists(os.path.join(student_path, 'a_file'))

        with mock.patch('sys.argv', args):
            main()

        assert os.path.exists(student_path)
        assert not os.path.exists(os.path.join(student_path, 'a_file'))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'repo_tests'))
def test_repo_reclone(datafiles):
    student_path = os.path.join(datafiles, 'students', 'cs251-specs')

    args = [sys.argv[0]] + ['repo', 'reclone', '--stogit', 'https://github.com/StoDevX', '--course', 'sd',
                            '--skip-version-check', '--skip-dependency-check']

    with chdir(str(datafiles)):
        assert not os.path.exists(student_path)
        clone_url('https://github.com/StoDevX/cs251-specs', student_path)
        touch(os.path.join(student_path, 'a_file'))
        assert os.path.exists(os.path.join(student_path, 'a_file'))

        with mock.patch('sys.argv', args):
            main()

        assert os.path.exists(student_path)
        assert not os.path.exists(os.path.join(student_path, 'a_file'))
