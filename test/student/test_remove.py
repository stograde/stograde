import os

from stograde.student import remove


def test_remove(tmpdir):
    with tmpdir.as_cwd():
        os.makedirs('test_dir')
        assert os.path.exists('test_dir')
        remove('test_dir')
        assert not os.path.exists('test_dir')
        remove('test_dir')
