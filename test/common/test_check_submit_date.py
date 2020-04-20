from stograde.common import check_dates
from stograde.specs.file_options import FileOptions
from stograde.specs.spec import Spec
from stograde.specs.spec_file import SpecFile
from test.common.test_find_unmerged_branches_in_cwd import git, touch


def test_check_dates_one_file_multiple_commits(tmpdir):
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

        date = check_dates(Spec('hw1', 'hw1', None, files=[SpecFile('test_file.txt', [], [], FileOptions())]),
                           '.')

    assert date == '04/17/20 09:31:00'


def test_check_dates_multiple_files(tmpdir):
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

        date = check_dates(Spec('hw1', 'hw1', None,
                                files=[SpecFile('test_file.txt', [], [], FileOptions()),
                                       SpecFile('test_file2.txt', [], [], FileOptions())]),
                           '.')

    assert date == '04/17/20 09:31:00'


def test_check_dates_files_missing(tmpdir):
    with tmpdir.as_cwd():
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('other_file.txt')
        git('add', 'other_file.txt')
        git('commit', '-m', '"add file"', '--date="Fri Apr 17 09:31:00 2020 -0500"')

        date = check_dates(Spec('hw1', 'hw1', None,
                                files=[SpecFile('test_file.txt', [], [], FileOptions()),
                                       SpecFile('test_file2.txt', [], [], FileOptions())]),
                           '.')

    assert date == 'ERROR: NO DATES'
