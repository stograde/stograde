from pyfakefs import fake_filesystem
from .dirsize import dirsize


def test_chdir(fs):
    os_module = fake_filesystem.FakeOsModule(fs)

    fs.create_dir('/folder')
    fs.create_file('/folder/file1', contents='0123456789')
    fs.create_file('/folder/file2', contents='0123456789')
    fs.create_file('/folder/file3', contents='0123456789')
    fs.create_file('/folder/file4', contents='0123456789')
    fs.create_file('/folder/file5', contents='0123456789')

    print(dirsize('/folder'))
