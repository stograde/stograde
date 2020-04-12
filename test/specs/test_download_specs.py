import os
import shutil
from unittest import mock

from stograde.specs.download_specs import download_specs, create_data_dir, get_supported_courses
from stograde.toolkit import global_vars


def test_download_specs(capsys):
    shutil.rmtree('data', ignore_errors=True)
    download_specs(course='sd', basedir='.')
    out, _ = capsys.readouterr()
    assert out == 'Downloading specs for SD\nDownload complete\n'
    shutil.rmtree('data')


def test_download_specs_bad_course(capsys):
    try:
        download_specs(course='bad', basedir='.')
    except SystemExit:
        pass

    _, err = capsys.readouterr()

    assert err == 'Course BAD not recognized\n'


def test_download_specs_failed_clone(capsys):
    os.makedirs('data', exist_ok=True)
    f = open('data/a_file.txt', 'w')
    f.write("I'm not empty")
    f.close()

    try:
        download_specs(course='sd', basedir='.')
    except SystemExit:
        pass

    _, err = capsys.readouterr()

    assert err == "Download failed: CALLED_PROCESS_ERROR: fatal: destination path 'data' " \
                  "already exists and is not an empty directory.\n\n"

    shutil.rmtree('data')


def test_create_data_dir_yes(capsys):
    shutil.rmtree('data', ignore_errors=True)
    with mock.patch('builtins.input', side_effect=['y', 'sd']):
        create_data_dir(course='', basedir='.')

    out, err = capsys.readouterr()

    assert err == 'data directory not found\n'
    assert out == 'Downloading specs for SD\nDownload complete\n'
    shutil.rmtree('data')


def test_create_data_dir_yes_but_no_course(capsys):
    try:
        with mock.patch('builtins.input', side_effect=['y', '']):
            create_data_dir(course='', basedir='.')
    except SystemExit:
        pass

    _, err = capsys.readouterr()

    assert err == 'data directory not found\nNot downloading specs\n'


def test_create_data_dir_no(capsys):
    try:
        with mock.patch('builtins.input', return_value='n'):
            create_data_dir(course='', basedir='.')
    except SystemExit:
        pass

    _, err = capsys.readouterr()

    assert err == 'data directory not found\nNot downloading specs\n'


def test_create_data_dir_ci(capsys):
    shutil.rmtree('data', ignore_errors=True)
    global_vars.CI = True
    create_data_dir(course='sd', basedir='.')
    out, _ = capsys.readouterr()
    assert out == 'Downloading specs for SD\nDownload complete\n'
    shutil.rmtree('data')
    global_vars.CI = False


def test_create_data_dir_ci_no_course(capsys):
    global_vars.CI = True
    try:
        create_data_dir(course='', basedir='.')
    except SystemExit:
        pass
    _, err = capsys.readouterr()
    assert err == 'data directory not found and no course specified\n'
    global_vars.CI = False


def test_get_supported_courses():
    assert get_supported_courses() == 'sd, hd, ads, os'
