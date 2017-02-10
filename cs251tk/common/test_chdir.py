from pyfakefs import fake_filesystem
from .chdir import chdir


def test_chdir(fs):
    os_module = fake_filesystem.FakeOsModule(fs)

    fs.CreateDirectory('./folder')

    assert os_module.getcwd() == '/'
    with chdir('./folder'):
        assert os_module.getcwd() == '/folder'
    assert os_module.getcwd() == '/'
