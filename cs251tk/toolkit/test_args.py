import datetime
from .args import (
    build_argparser,
    get_students_from_args,
    get_assignments_from_args,
    compute_stogit_url,
)


def args(arglist):
    return vars(build_argparser().parse_args(args=arglist))


students = {
    'my': ['rives'],
    'section-a': ['student-a'],
    'section-b': ['student-b'],
}


def test_all():
    # check that --all includes all students
    assert get_students_from_args(**args(['--all']), _all_students=students) == students['my'] + students['section-a'] + students['section-b']


def test_students():
    # multiple sets of --students should wind up as one flattened list
    assert get_students_from_args(**args(['--students', 'a', 'b', '--students', 'c']), _all_students=students) == ['a', 'b', 'c']

    # it should return a sorted list of student names
    assert get_students_from_args(**args(['--students', 'c', 'b', '--students', 'a']), _all_students=students) == ['a', 'b', 'c']

    # multiple occurences of the same student should be removed
    assert get_students_from_args(**args(['--students', 'a', 'a', '--students', 'a']), _all_students=students) == ['a']

    # if no students are given, it should default to the "my" section
    assert get_students_from_args(**args([]), _all_students=students) == students['my']


def test_section():
    # "--section $name" should return the students for that section
    assert get_students_from_args(**args(['--section', 'a']), _all_students=students) == students['section-a']


def test_record():
    assert get_assignments_from_args(**args(['--record', 'hw4'])) == ['hw4']


def test_stogit_url_computation():
    assert compute_stogit_url(stogit=None, course='sd', _now=datetime.date(2017, 1, 31)) \
        == 'git@stogit.cs.stolaf.edu:sd-s17'

    assert compute_stogit_url(stogit=None, course='sd', _now=datetime.date(2016, 9, 15)) \
        == 'git@stogit.cs.stolaf.edu:sd-f16'

    assert compute_stogit_url(stogit=None, course='sd', _now=datetime.date(2016, 4, 15)) \
        == 'git@stogit.cs.stolaf.edu:sd-s16'

    assert compute_stogit_url(stogit='blah', course='sd', _now=datetime.date.today()) \
        == 'blah'

    assert compute_stogit_url(stogit=None, course='hd', _now=datetime.date(2016, 4, 15)) \
        == 'git@stogit.cs.stolaf.edu:hd-s16'
