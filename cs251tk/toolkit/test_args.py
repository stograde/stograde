from .args import get_args, massage_args


def args(arglist):
    return vars(get_args().parse_args(args=arglist))


students = {
    'my': ['rives'],
    'section-a': ['student-a'],
    'section-b': ['student-b'],
}


def test_all():
    # check that --all sets `all` to true
    assert massage_args(args([]), students)['all'] == False
    assert massage_args(args(['--all']), students)['all'] == True

    # check that --all includes all students
    assert massage_args(args(['--all']), students)['students'] == students['my'] + students['section-a'] + students['section-b']


def test_students():
    # multiple sets of --students should wind up as one flattened list
    assert massage_args(args(['--students', 'a', 'b', '--students', 'c']), students)['students'] == ['a', 'b', 'c']

    # it should return a sorted list of student names
    assert massage_args(args(['--students', 'c', 'b', '--students', 'a']), students)['students'] == ['a', 'b', 'c']

    # multiple occurences of the same student should be removed
    assert massage_args(args(['--students', 'a', 'a', '--students', 'a']), students)['students'] == ['a']

    # if no students are given, it should default to the "my" section
    assert massage_args(args([]), students)['section'] == ['my']


def test_section():
    # "--section $name" should return the students for that section
    assert massage_args(args(['--section', 'a']), students)['students'] == students['section-a']


def test_record():
    assert massage_args(args(['--record', 'hw4']), students)['record'] == ['hw4']
