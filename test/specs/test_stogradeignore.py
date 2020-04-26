import logging
import os

import pytest

from stograde.common import chdir
from stograde.specs.stogradeignore import load_stogradeignore

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'stogradeignore'))
def test_load_stogradeignore(datafiles, caplog):
    with caplog.at_level(logging.DEBUG):
        with chdir(str(datafiles)):
            assignments = load_stogradeignore()

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {("Ignored specs: ['hw1', 'lab23', 'ws4', 'lab5']", 'DEBUG')}

    assert set(assignments) == {'hw1', 'lab5', 'lab23', 'ws4'}


def test_load_stogradeignore_file_not_found(caplog):
    with caplog.at_level(logging.DEBUG):
        assignments = load_stogradeignore()

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('No .stogradeignore file found', 'DEBUG')}

    assert isinstance(assignments, list)
    assert not assignments
