import os

from stograde.common import get_assignment_first_submit_time, get_modification_time
from stograde.common.modification_time import ModificationTime
from stograde.specs.file_options import FileOptions
from stograde.specs.spec import Spec
from stograde.specs.spec_file import SpecFile
from test.utils import git, touch


def test_get_modification_time_first(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('test_file.txt')
        git('add', 'test_file.txt')
        git('commit', '-m', '"add file"', '--date="Fri Apr 17 09:31:00 2020 -0500"')

        # Add another commit to prove that it is finding the first
        with open('test_file.txt', 'a') as file:
            file.write('add content')
            file.close()
        git('add', 'test_file.txt')
        git('commit', '-m', '"update file"', '--date="Sat Apr 25 17:18:33 2020 -0500"')

        date, iso = get_modification_time('test_file.txt', os.getcwd(), ModificationTime.FIRST)

    assert date == 'Fri Apr 17 09:31:00 2020 -0500'
    assert iso == '2020-04-17 09:31:00 -0500'


def test_get_modification_time_latest(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('test_file.txt')
        git('add', 'test_file.txt')
        git('commit', '-m', '"add file"', '--date="Fri Apr 17 09:31:00 2020 -0500"')

        # Add another commit to prove that it is finding the latest
        with open('test_file.txt', 'a') as file:
            file.write('add content')
            file.close()
        git('add', 'test_file.txt')
        git('commit', '-m', '"update file"', '--date="Sat Apr 25 17:18:33 2020 -0500"')

        date, iso = get_modification_time('test_file.txt', os.getcwd(), ModificationTime.LATEST)

    assert date == 'Sat Apr 25 17:18:33 2020 -0500'
    assert iso == '2020-04-25 17:18:33 -0500'


def test_get_modification_time_file_missing(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('other_file.txt')
        git('add', 'other_file.txt')
        git('commit', '-m', '"add file"', '--date="Fri Apr 17 09:31:00 2020 -0500"')

        date, iso = get_modification_time('test_file.txt', os.getcwd())

    assert not date
    assert not iso


def test_first_submit_one_file_multiple_commits(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('test_file.txt')
        git('add', 'test_file.txt')
        git('commit', '-m', '"add file"', '--date="Fri Apr 17 09:31:00 2020 -0500"')

        # Add another commit to prove that it is finding the first
        with open('test_file.txt', 'a') as file:
            file.write('add content')
            file.close()
        git('add', 'test_file.txt')
        git('commit', '-m', '"update file"')

        date = get_assignment_first_submit_time(
            Spec('hw1', 'hw1', None, files=[SpecFile('test_file.txt', [], [], FileOptions())]),
            '.')

    assert date == 'Fri Apr 17 09:31:00 2020 -0500'


def test_first_submit_multiple_files(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('test_file.txt')
        git('add', 'test_file.txt')
        git('commit', '-m', '"add file"', '--date="Fri Apr 17 09:31:00 2020 -0500"')

        touch('test_file2.txt')
        git('add', 'test_file2.txt')
        git('commit', '-m', '"add other file"', '--date="Sat Apr 18 16:12:14 2020 -0500')

        date = get_assignment_first_submit_time(
            Spec('hw1', 'hw1', None,
                 files=[SpecFile('test_file.txt', [], [], FileOptions()),
                        SpecFile('test_file2.txt', [], [], FileOptions())]),
            '.')

    assert date == 'Fri Apr 17 09:31:00 2020 -0500'


def test_first_submit_some_files_missing(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('test_file.txt')
        git('add', 'test_file.txt')
        git('commit', '-m', '"add file"', '--date="Fri Apr 17 09:31:00 2020 -0500"')

        date = get_assignment_first_submit_time(
            Spec('hw1', 'hw1', None,
                 files=[SpecFile('test_file.txt', [], [], FileOptions()),
                        SpecFile('test_file2.txt', [], [], FileOptions())]),
            '.')

    assert date == 'Fri Apr 17 09:31:00 2020 -0500'


def test_first_submit_all_files_missing(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('other_file.txt')
        git('add', 'other_file.txt')
        git('commit', '-m', '"add file"', '--date="Fri Apr 17 09:31:00 2020 -0500"')

        date = get_assignment_first_submit_time(
            Spec('hw1', 'hw1', None,
                 files=[SpecFile('test_file.txt', [], [], FileOptions()),
                        SpecFile('test_file2.txt', [], [], FileOptions())]),
            '.')

    assert date == 'ERROR: NO DATES'
