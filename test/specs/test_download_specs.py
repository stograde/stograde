import os
from unittest import mock

from stograde.specs.download_specs import download_specs, create_data_dir


def test_download_specs(tmpdir, capsys):
    with tmpdir.as_cwd():
        download_specs(course='sd', basedir='.')

    out, err = capsys.readouterr()

    assert out == 'Downloading specs for SD\nDownload complete\n'
    assert err == ''


def test_download_specs_bad_course(capsys):
    try:
        download_specs(course='bad', basedir='.')
        raise AssertionError
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == ''
    assert err == 'Invalid course: BAD\n'


def test_download_specs_failed_clone(tmpdir, capsys):
    with tmpdir.as_cwd():
        os.makedirs('data')
        f = open('data/a_file.txt', 'w')
        f.write("I'm not empty")
        f.close()

        try:
            download_specs(course='sd', basedir='.')
            raise AssertionError
        except SystemExit:
            pass

    out, err = capsys.readouterr()

    assert out == 'Downloading specs for SD\n'
    assert err == ("Downloading specs for SD failed: CALLED_PROCESS_ERROR: fatal: destination path 'data' "
                   'already exists and is not an empty directory.\n\n')


@mock.patch('stograde.toolkit.global_vars.CI', True)
def test_download_specs_ci_failed_clone(tmpdir, capsys):
    with tmpdir.as_cwd():
        os.makedirs('data')
        f = open('data/a_file.txt', 'w')
        f.write("I'm not empty")
        f.close()

        try:
            download_specs(course='sd', basedir='.')
            raise AssertionError
        except SystemExit:
            pass

    out, err = capsys.readouterr()

    assert out == ''
    assert err == ("Downloading specs for SD failed: CALLED_PROCESS_ERROR: fatal: destination path 'data' "
                   'already exists and is not an empty directory.\n\n')


def test_create_data_dir(tmpdir, capsys):
    with tmpdir.as_cwd():
        with mock.patch('builtins.input', side_effect=['y', 'sd']):
            create_data_dir(course='sd', basedir='.')

    out, err = capsys.readouterr()

    assert out == 'Downloading specs for SD\nDownload complete\n'
    assert err == 'data directory not found\n'


def test_create_data_dir_yes(tmpdir, capsys):
    with tmpdir.as_cwd():
        with mock.patch('builtins.input', side_effect=['y', 'sd']):
            create_data_dir(course='', basedir='.')

    out, err = capsys.readouterr()

    assert out == 'Downloading specs for SD\nDownload complete\n'
    assert err == 'data directory not found\n'


def test_create_data_dir_yes_but_no_course(capsys):
    try:
        with mock.patch('builtins.input', side_effect=['y', '']):
            create_data_dir(course='', basedir='.')
            raise AssertionError
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == ''
    assert err == 'data directory not found\nNot downloading specs\n'


def test_create_data_dir_no(capsys):
    try:
        with mock.patch('builtins.input', return_value='n'):
            create_data_dir(course='', basedir='.')
            raise AssertionError
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == ''
    assert err == 'data directory not found\nNot downloading specs\n'


@mock.patch('stograde.toolkit.global_vars.CI', True)
def test_create_data_dir_ci(tmpdir, capsys):
    with tmpdir.as_cwd():
        create_data_dir(course='sd', basedir='.')

    out, err = capsys.readouterr()

    assert out == ''
    assert err == ''


@mock.patch('stograde.toolkit.global_vars.CI', True)
def test_create_data_dir_ci_no_course(capsys):
    try:
        create_data_dir(course='', basedir='.')
        raise AssertionError
    except SystemExit:
        pass

    out, err = capsys.readouterr()

    assert out == ''
    assert err == 'data directory not found and no course specified\n'
