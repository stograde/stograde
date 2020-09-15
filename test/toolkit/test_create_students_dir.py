import os

from stograde.toolkit.create_students_dir import create_students_dir


def test_create_students_dir(tmpdir):
    with tmpdir.as_cwd():
        create_students_dir(os.getcwd())

        assert os.path.exists('students')
