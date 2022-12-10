import os.path

from stograde.common.dirsize import dirsize


def test_dirsize(fs):
    fs.create_dir('/folder')
    fs.create_file('/folder/file1', contents='0123456789')
    fs.create_file('/folder/file2', contents='0123456789')
    fs.create_file('/folder/file3', contents='0123456789')
    fs.create_file('/folder/file4', contents='0123456789')
    fs.create_file('/folder/file5', contents='0123456789')

    assert dirsize('/folder') == 50


def test_dirsize_fail(fs):
    fs.create_dir('/folder')

    assert not os.path.exists("/folder/subfolder")

    assert dirsize('/folder/subfolder') == 0
