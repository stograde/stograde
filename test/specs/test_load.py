import os

import pytest

from stograde.common import chdir
from stograde.specs import load_specs
from stograde.specs.load import check_for_spec_updates
from test.utils import git

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_load_specs(datafiles):
    specs = load_specs(['hw1', 'hw2', 'hw3'], str(datafiles), skip_spec_update=True)

    assert len(specs) == 3


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_load_specs_failed_update(datafiles, capsys):
    specs = load_specs(['hw1', 'hw2', 'hw3'], str(datafiles), skip_spec_update=False)

    assert len(specs) == 3

    _, err = capsys.readouterr()

    assert err == 'Error fetching specs\ngit log failed\n'


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'updated_specs'))
def test_check_for_spec_updates(datafiles, capsys):
    with chdir(str(datafiles)):
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')
        git('add', 'hw1.yaml')
        git('commit', '-m', '"Add hw1"')
        git('branch', 'origin/master')
        git('checkout', 'origin/master')
        with open('hw2.yaml', 'w') as hw2:
            hw2.write('---\nassignment: hw2\n')
        git('add', 'hw2.yaml')
        git('commit', '-m', '"Create hw2"')
        git('checkout', 'master')

    check_for_spec_updates(str(datafiles))

    _, err = capsys.readouterr()

    assert err == 'Error fetching specs\nSpec updates found - Updating\n'
