import sys
from unittest import mock

from stograde.toolkit.__main__ import main


def test_main_version_check_output(capsys):
    args = [sys.argv[0]] + ['record', 'hw1', '--student', 'student1',
                            '--skip-repo-update', '--skip-spec-update', '--skip-dependency-check']

    with mock.patch('stograde.toolkit.__main__.update_available', return_value=('Old', 'New')):
        with mock.patch('stograde.toolkit.__main__.create_data_dir', side_effect=ValueError()):
            with mock.patch('sys.argv', args):
                try:
                    main()
                    raise AssertionError
                except ValueError:
                    pass

    _, err = capsys.readouterr()

    assert err == ('vNew is available: you have vOld. '
                   'Try "pip3 install --no-cache --user --upgrade stograde" to update.\n')


def test_main_dependency_check():
    args = [sys.argv[0]] + ['record', 'hw1', '--student', 'student1', '--skip-version-check',
                            '--skip-repo-update', '--skip-spec-update']

    with mock.patch('stograde.toolkit.__main__.check_dependencies') as mock_check:
        with mock.patch('stograde.toolkit.__main__.create_data_dir', side_effect=ValueError()):
            with mock.patch('sys.argv', args):
                try:
                    main()
                    raise AssertionError
                except ValueError:
                    pass
        assert mock_check.called

    args = [sys.argv[0]] + ['record', 'hw1', '--student', 'student1', '--skip-version-check',
                            '--skip-repo-update', '--skip-spec-update', '--skip-dependency-check']

    with mock.patch('stograde.toolkit.__main__.check_dependencies') as mock_check:
        with mock.patch('stograde.toolkit.__main__.create_data_dir', side_effect=ValueError()):
            with mock.patch('sys.argv', args):
                try:
                    main()
                    raise AssertionError
                except ValueError:
                    pass
        assert not mock_check.called


def test_main_date(capsys):
    args = [sys.argv[0]] + ['record', 'hw1', '--student', 'student1', '--date', 'a date', '--skip-version-check',
                            '--skip-repo-update', '--skip-spec-update', '--skip-dependency-check']

    with mock.patch('stograde.toolkit.__main__.create_data_dir'):
        with mock.patch('stograde.toolkit.__main__.compute_stogit_url'):
            with mock.patch('stograde.toolkit.__main__.create_students_dir'):
                with mock.patch('stograde.toolkit.__main__.filter_assignments', side_effect=ValueError()):
                    with mock.patch('sys.argv', args):
                        try:
                            main()
                            raise AssertionError
                        except ValueError:
                            pass

    out, _ = capsys.readouterr()

    assert out == 'Checking out a date\n'


def test_main_no_specs_loaded(capsys):
    args = [sys.argv[0]] + ['record', 'hw1', '--student', 'student1', '--date', 'a date', '--skip-version-check',
                            '--skip-repo-update', '--skip-spec-update', '--skip-dependency-check']

    with mock.patch('stograde.toolkit.__main__.create_data_dir'):
        with mock.patch('stograde.toolkit.__main__.compute_stogit_url'):
            with mock.patch('stograde.toolkit.__main__.create_students_dir'):
                with mock.patch('stograde.toolkit.__main__.filter_assignments'):
                    with mock.patch('stograde.toolkit.__main__.load_specs', return_value=[]):
                        with mock.patch('sys.argv', args):
                            try:
                                main()
                                raise AssertionError
                            except SystemExit:
                                pass

    _, err = capsys.readouterr()

    assert err == 'No specs loaded!\n'
