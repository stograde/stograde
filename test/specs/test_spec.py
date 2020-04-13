import os

import pytest

from stograde.common import chdir
from stograde.specs.spec import create_spec

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_no_assignment(datafiles):
    with chdir(str(datafiles)):
        try:
            create_spec(os.path.join(datafiles, 'spec_no_assignment.yaml'), '.')
        except AssertionError:
            pass


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_simple_assignment(datafiles):
    with chdir(str(datafiles)):
        new_spec = create_spec(os.path.join(datafiles, 'spec_simple_assignment.yaml'), '.')

    assert new_spec.id == 'hw1'
    assert new_spec.folder == 'hw1'
    assert new_spec.architecture is None
    assert not new_spec.dependencies
    assert not new_spec.files
    assert not new_spec.supporting_files


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_with_folder(datafiles):
    with chdir(str(datafiles)):
        new_spec = create_spec(os.path.join(datafiles, 'spec_with_folder.yaml'), '.')

    assert new_spec.id == 'hw2'
    assert new_spec.folder == 'some_other_folder'
    assert new_spec.architecture is None
    assert not new_spec.dependencies
    assert not new_spec.files
    assert not new_spec.supporting_files


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_with_architecture(datafiles):
    with chdir(str(datafiles)):
        new_spec = create_spec(os.path.join(datafiles, 'spec_with_architecture.yaml'), '.')

    assert new_spec.id == 'hw3'
    assert new_spec.folder == 'hw3'
    assert new_spec.architecture == 'armv7l'
    assert not new_spec.dependencies
    assert not new_spec.files
    assert not new_spec.supporting_files


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_with_files(datafiles):
    with chdir(str(datafiles)):
        new_spec = create_spec(os.path.join(datafiles, 'spec_with_files.yaml'), '.')

    assert new_spec.id == 'hw4'
    assert new_spec.folder == 'hw4'
    assert new_spec.architecture is None
    assert not new_spec.dependencies
    assert new_spec.files
    assert len(new_spec.files) == 2
    assert not new_spec.supporting_files


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_with_dependencies_list(datafiles):
    with chdir(str(datafiles)):
        new_spec = create_spec(os.path.join(datafiles, 'spec_with_dependencies_list.yaml'), '.')

    assert new_spec.id == 'hw5'
    assert new_spec.folder == 'hw5'
    assert new_spec.architecture is None
    assert new_spec.dependencies
    assert len(new_spec.dependencies) == 2
    assert 'dependency1' in new_spec.dependencies
    assert 'dependency2' in new_spec.dependencies
    assert not new_spec.files
    assert not new_spec.supporting_files


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_with_dependencies_str(datafiles):
    with chdir(str(datafiles)):
        new_spec = create_spec(os.path.join(datafiles, 'spec_with_dependencies_str.yaml'), '.')

    assert new_spec.id == 'hw6'
    assert new_spec.folder == 'hw6'
    assert new_spec.architecture is None
    assert new_spec.dependencies
    assert len(new_spec.dependencies) == 1
    assert 'dependency3' in new_spec.dependencies
    assert not new_spec.files
    assert not new_spec.supporting_files


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_with_supporting(datafiles):
    with chdir(str(datafiles)):
        new_spec = create_spec(os.path.join(datafiles, 'spec_with_supporting.yaml'), '.')

    assert new_spec.id == 'hw7'
    assert new_spec.folder == 'hw7'
    assert new_spec.architecture is None
    assert new_spec.dependencies is None
    assert not new_spec.files
    assert new_spec.supporting_files
    assert len(new_spec.supporting_files) == 2


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_with_supporting(datafiles):
    with chdir(str(datafiles)):
        new_spec = create_spec(os.path.join(datafiles, 'spec_with_inputs.yaml'), '.')

    assert new_spec.id == 'hw8'
    assert new_spec.folder == 'hw8'
    assert new_spec.architecture is None
    assert not new_spec.dependencies
    assert not new_spec.files
    assert new_spec.supporting_files
    assert len(new_spec.supporting_files) == 2


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_with_supporting(datafiles):
    with chdir(str(datafiles)):
        new_spec = create_spec(os.path.join(datafiles, 'spec_with_supporting_and_inputs.yaml'), '.')

    assert new_spec.id == 'hw9'
    assert new_spec.folder == 'hw9'
    assert new_spec.architecture is None
    assert not new_spec.dependencies
    assert not new_spec.files
    assert new_spec.supporting_files
    assert len(new_spec.supporting_files) == 4


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'create_spec'))
def test_create_spec_with_legacy_tests(datafiles):
    with chdir(str(datafiles)):
        new_spec = create_spec(os.path.join(datafiles, 'spec_with_legacy_tests.yaml'), '.')

    assert new_spec.id == 'hw10'
    assert new_spec.folder == 'hw10'
    assert new_spec.architecture is None
    assert not new_spec.dependencies
    assert new_spec.files
    assert new_spec.files[0].file_name == 'test_file1.txt'
    assert len(new_spec.files[0].test_commands) == 1
    assert new_spec.files[1].file_name == 'test_file2.txt'
    assert len(new_spec.files[1].test_commands) == 2
    assert not new_spec.supporting_files
