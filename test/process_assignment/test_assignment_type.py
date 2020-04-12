from stograde.process_assignment.assignment_type import AssignmentType, get_assignment_type, get_assignment_number, \
    parse_assignment_name


def test_get_assignment_type():
    assert get_assignment_type('hw1') is AssignmentType.HOMEWORK
    assert get_assignment_type('lab23') is AssignmentType.LAB
    assert get_assignment_type('ws4') is AssignmentType.WORKSHEET


def test_get_assignment_number():
    assert get_assignment_number('hw132') == 132
    assert get_assignment_number('lab1') == 1
    assert get_assignment_number('ws32') == 32


def test_parse_assignment_name():
    assert parse_assignment_name('hw21') == ('hw', '21')
    assert parse_assignment_name('lab2') == ('lab', '2')
    assert parse_assignment_name('ws212') == ('ws', '212')
    try:
        parse_assignment_name('bad32')
    except ValueError:
        pass
