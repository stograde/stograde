from textwrap import dedent
from .tabulate import find_columns, pad, MISSING, concat, symbol, columnize, get_nums, sort_by_hw_count, sort_by_username, tabulate


def test_pad():
    assert pad("HW2", 12345) == "HW2  ", "should pad to the left to the width of the number"
    assert pad("HW2", 1) == "HW2", "should not trim the string if the number is shorter"
    assert pad(MISSING, 12345) == (MISSING * 5), "should use MISSING if given"


def test_find_columns():
    assert find_columns(10) == "1 2 3 4 5 6 7 8 9 10", "should return incremental numbers between 1 and the argument"


def test_symbol():
    assert symbol({'number': 5, 'status': 'success'}) == '5', "return the number for sucessful assignments"
    assert symbol({'number': 5, 'status': 'missing'}) == MISSING, "returns MISSING for missing assignments"
    assert symbol({'number': 5, 'status': 'partial'}) == '5', "returns the raw number ift stdout can't handle fanciness"


def test_concat():
    assert concat([
        {'number': 1, 'status': 'success'},
        {'number': 2, 'status': 'success'},
    ], 2) == "1 2", "should turn an assignment list into a string"

    assert concat([
        {'number': 1, 'status': 'success'},
        {'number': 2, 'status': 'success'},
    ], 6) == "1 2 - - - -", "should output hyphens when no assignments are given"

    assert concat([
        {'number': 1, 'status': 'success'},
        {'number': 6, 'status': 'success'},
    ], 6) == "1 - - - - 6", "should handle missing assignments in between others"

    assert concat([
        {'number': 10, 'status': 'success'},
        {'number': 11, 'status': 'success'},
    ], 12) == "- - - - - - - - - 10 11 --", "should output two hyphens for two-digit numbers"


def test_columnize():
    student = {
        'username': 'rives',
        'unmerged_branches': False,
        'homeworks': [
            {'number': 1, 'status': 'success'},
            {'number': 2, 'status': 'success'},
        ],
        'labs': [
            {'number': 1, 'status': 'success'},
        ]
    }

    assert columnize(student, 'rives', 2, 1) == "rives  | 1 2 | 1"
    assert columnize(student, 'long_username', 2, 1) == "rives          | 1 2 | 1"
    assert columnize(student, 'rives', 5, 1) == "rives  | 1 2 - - - | 1"
    assert columnize(student, 'rives', 2, 5) == "rives  | 1 2 | 1 - - - -"

    student2 = {
        'username': 'rives',
        'unmerged_branches': True,
        'homeworks': [
            {'number': 1, 'status': 'success'},
            {'number': 2, 'status': 'success'},
        ],
        'labs': [
            {'number': 1, 'status': 'success'},
        ]
    }

    assert columnize(student2, 'rives', 2, 1) == "\033[1mrives\033[0m  | 1 2 | 1"

    student3 = {
        'username': 'rives',
        'error': 'an error occurred',
        'homeworks': [],
        'labs': [],
    }

    assert columnize(student3, 'rives', 2, 1) == "{username}  | {error}".format(**student3)

    student4 = {
        'username': 'rives',
        'error': 'an error occurred',
    }

    assert columnize(student4, 'rives', 0, 0) == "{username}  | {error}".format(**student4)


def test_get_nums():
    assert get_nums([
        {
            'username': 'rives',
            'unmerged_branches': True,
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
            ],
            'labs': [
                {'number': 1, 'status': 'success'},
            ]
        }
    ]) == (2, 1)

    assert get_nums([
        {
            'username': 'rives1',
            'unmerged_branches': True,
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
            ],
            'labs': [
                {'number': 1, 'status': 'success'},
            ]
        },
        {
            'username': 'rives2',
            'unmerged_branches': True,
            'homeworks': [
                {'number': 8, 'status': 'success'},
                {'number': 9, 'status': 'success'},
            ],
            'labs': [
                {'number': 10, 'status': 'success'},
            ]
        }
    ]) == (9, 10)

    assert get_nums([
        {
            'username': 'student',
            'unmerged_branches': True,
            'homeworks': [],
            'labs': [],
        }
    ]) == (0, 0)

    assert get_nums([
        {
            'username': 'student',
            'unmerged_branches': True,
            'homeworks': [
                {'number': 1, 'status': 'success'},
            ],
            'labs': [],
        }
    ]) == (1, 0)

    assert get_nums([
        {
            'username': 'student',
            'unmerged_branches': True,
            'homeworks': [],
            'labs': [
                {'number': 1, 'status': 'success'},
            ],
        }
    ]) == (0, 1)


def test_sort_by_hw_count():
    students = [
        {
            'username': 'rives1',
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
                {'number': 3, 'status': 'success'},
                {'number': 4, 'status': 'success'},
            ],
        },
        {
            'username': 'rives2',
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
                {'number': 3, 'status': 'success'},
            ],
        },
        {
            'username': 'rives3',
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
            ],
        },
    ]

    assert sorted(students, key=sort_by_hw_count) == list(reversed(students))


def test_sort_by_username():
    students = [
        {
            'username': 'rives1',
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
                {'number': 3, 'status': 'success'},
                {'number': 4, 'status': 'success'},
            ],
        },
        {
            'username': 'rives2',
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
                {'number': 3, 'status': 'success'},
            ],
        },
        {
            'username': 'rives3',
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
            ],
        },
    ]

    assert sorted(students, key=sort_by_username) == students


def test_tabulate():
    students = [
        {
            'username': 'rives3',
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
                {'number': 3, 'status': 'success'},
                {'number': 4, 'status': 'success'},
            ],
        },
        {
            'username': 'rives2',
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
                {'number': 3, 'status': 'success'},
            ],
        },
        {
            'username': 'rives1',
            'homeworks': [
                {'number': 1, 'status': 'success'},
                {'number': 2, 'status': 'success'},
            ],
            'labs': [
                {'number': 1, 'status': 'success'},
            ]
        },
    ]

    assert tabulate(students) == dedent("""
    USER    | 1 2 3 4 | 1
    --------+---------+--
    rives1  | 1 2 - - | 1
    rives2  | 1 2 3 - | -
    rives3  | 1 2 3 4 | -
    """).strip()

    assert tabulate(students, sort_by='count') == dedent("""
    USER    | 1 2 3 4 | 1
    --------+---------+--
    rives3  | 1 2 3 4 | -
    rives2  | 1 2 3 - | -
    rives1  | 1 2 - - | 1
    """).strip()
