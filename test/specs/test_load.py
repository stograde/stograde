import os

import pytest

from stograde.specs import load_specs

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_load_specs(datafiles):
    specs = load_specs(['hw1', 'hw2', 'hw3'], str(datafiles), skip_spec_update=True)

    assert len(specs) == 3
