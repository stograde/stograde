import datetime

from stograde.toolkit.stogit_url import compute_stogit_url


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
