import datetime
import shutil

from stograde.common import run
from stograde.toolkit.stogit_url import compute_stogit_url, get_course_from_specs


def test_stogit_url_computation():
    assert compute_stogit_url(stogit='', course='sd', _now=datetime.date(2017, 1, 31)) \
        == 'git@stogit.cs.stolaf.edu:sd/s17'

    assert compute_stogit_url(stogit='', course='sd', _now=datetime.date(2016, 9, 15)) \
        == 'git@stogit.cs.stolaf.edu:sd/f16'

    assert compute_stogit_url(stogit='', course='sd', _now=datetime.date(2016, 4, 15)) \
        == 'git@stogit.cs.stolaf.edu:sd/s16'

    assert compute_stogit_url(stogit='blah', course='sd', _now=datetime.date.today()) \
        == 'blah'

    assert compute_stogit_url(stogit='', course='hd', _now=datetime.date(2016, 4, 15)) \
        == 'git@stogit.cs.stolaf.edu:hd/s16'


def test_get_course_from_specs_success():
    shutil.rmtree('data', ignore_errors=True)
    run(['git', 'clone', 'https://github.com/StoDevX/cs251-specs.git', 'data'])
    course = get_course_from_specs()
    assert course == 'sd'
    shutil.rmtree('data')


def test_get_course_from_specs_failure(capsys):
    shutil.rmtree('data', ignore_errors=True)
    try:
        get_course_from_specs()
    except SystemExit:
        pass

    _, err = capsys.readouterr()

    assert err == 'Cannot determine course from specs\n'
