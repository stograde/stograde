import logging
import os

import pytest

from stograde.common import chdir
from stograde.specs import filter_assignments
from stograde.specs.filter_specs import get_spec_paths, find_all_specs, filter_loaded_specs
from stograde.specs.spec import Spec
from stograde.specs.util import get_user_architecture
from stograde.toolkit import global_vars

_dir = os.path.dirname(os.path.realpath(__file__))


def test_filter_assignments_no_ci():
    global_vars.CI = False
    assignments = ['hw1', 'hw2']
    assert filter_assignments(assignments) == assignments


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'stogradeignore'))
def test_filter_assignments_ci_some(datafiles, caplog):
    global_vars.CI = True
    assignments = ['hw1', 'hw2']

    with chdir(str(datafiles)):
        assert filter_assignments(assignments) == ['hw2']

    log_messages = {log.msg for log in caplog.records}

    assert log_messages == {'Skipping hw1: ignored by stogradeignore'}

    for log in caplog.records:
        assert log.levelname == 'WARNING'

    global_vars.CI = False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'stogradeignore'))
def test_filter_assignments_ci_all(datafiles, caplog):
    global_vars.CI = True
    assignments = ['hw1', 'lab5']

    with chdir(str(datafiles)):
        assert not filter_assignments(assignments)

    log_messages = {log.msg for log in caplog.records}

    assert log_messages == {'Skipping hw1: ignored by stogradeignore',
                            'Skipping lab5: ignored by stogradeignore',
                            'All assignments ignored by stogradeignore'}

    for log in caplog.records:
        assert log.levelname == 'WARNING'

    global_vars.CI = False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'get_spec_paths'))
def test_get_spec_paths_all_present(datafiles):
    wanted_assignments = ['hw1']

    with chdir(str(datafiles)):
        paths = get_spec_paths(wanted_assignments, str(datafiles))

    assert set(paths) == {os.path.join(datafiles, 'hw1.yaml')}


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'get_spec_paths'))
def test_get_spec_paths_some_missing(datafiles, caplog):
    wanted_assignments = ['hw1', 'hw4']

    with chdir(str(datafiles)):
        paths = get_spec_paths(wanted_assignments, str(datafiles))

    assert set(paths) == {os.path.join(datafiles, 'hw1.yaml')}

    log_messages = {log.msg for log in caplog.records}

    assert log_messages == {'No spec for hw4'}

    for log in caplog.records:
        assert log.levelname == 'WARNING'


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'get_spec_paths'))
def test_find_all_specs(datafiles):
    with chdir(str(datafiles)):
        assert set(find_all_specs(str(datafiles))) == {os.path.join(datafiles, 'hw1.yaml'),
                                                       os.path.join(datafiles, 'hw2.yaml'),
                                                       os.path.join(datafiles, 'hw3.yaml')}


def test_filter_loaded_specs():
    specs = {
        'hw1': Spec(id='hw1', folder='hw1', architecture=None),
        'hw2': Spec(id='hw2', folder='hw2', architecture=None),
    }

    filtered_specs = filter_loaded_specs(specs)

    assert filtered_specs == specs


def test_filter_loaded_specs_wrong_architecture(capsys):
    specs = {
        'hw1': Spec(id='hw1', folder='hw1', architecture='totallynottherightarchitecture')
    }

    filtered_specs = filter_loaded_specs(specs)

    _, err = capsys.readouterr()

    assert isinstance(filtered_specs, dict)
    assert not filtered_specs
    assert err == 'hw1 requires totallynottherightarchitecture architecture. ' \
                  'You have {}\n'.format(get_user_architecture())


def test_filter_loaded_specs_wrong_architecture_ci(caplog):
    global_vars.CI = True
    specs = {
        'hw1': Spec(id='hw1', folder='hw1', architecture='totallynottherightarchitecture')
    }

    filtered_specs = filter_loaded_specs(specs)

    log_messages = {log.msg for log in caplog.records}

    assert isinstance(filtered_specs, dict)
    assert not filtered_specs
    assert log_messages == {'Skipping hw1: wrong architecture'}

    for log in caplog.records:
        assert log.levelname == 'WARNING'

    global_vars.CI = False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'get_spec_paths'))
def test_filter_loaded_specs_present_dependency(datafiles):
    specs = {
        'hw1': Spec(id='hw1', folder='hw1', architecture=None, dependencies=[os.path.join(datafiles, 'hw1.yaml')])
    }

    filtered_specs = filter_loaded_specs(specs)

    assert filtered_specs == specs


def test_filter_loaded_specs_missing_dependency(caplog):
    specs = {
        'hw1': Spec(id='hw1', folder='hw1', architecture=None, dependencies=['definitelymissingdependency.txt'])
    }

    filtered_specs = filter_loaded_specs(specs)

    log_messages = {log.msg for log in caplog.records}

    assert isinstance(filtered_specs, dict)
    assert not filtered_specs
    assert log_messages == {'Skipping hw1: required file "definitelymissingdependency.txt" could not be found'}

    for log in caplog.records:
        assert log.levelname == 'WARNING'
