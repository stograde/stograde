from textwrap import dedent

from stograde.process_assignment.Assignment_Status import AssignmentStatus
from stograde.student.Student_Result import StudentResult
from stograde.toolkit.tabulate import find_columns, pad, MISSING, concat, symbol, columnize, get_nums, sort_by_hw_count, \
    sort_by_username, tabulate


def test_pad():
    assert pad("HW2", 12345) == "HW2  ", "should pad to the left to the width of the number"
    assert pad("HW2", 1) == "HW2", "should not trim the string if the number is shorter"
    assert pad(MISSING, 12345) == (MISSING * 5), "should use MISSING if given"


def test_find_columns():
    assert find_columns(10) == "1 2 3 4 5 6 7 8 9 10", "should return incremental numbers between 1 and the argument"


def test_symbol():
    assert symbol((5, AssignmentStatus.SUCCESS)) == '5', "return the number for successful assignments"
    assert symbol((5, AssignmentStatus.MISSING)) == MISSING, "returns MISSING for missing assignments"
    assert symbol((5, AssignmentStatus.PARTIAL)) == '5', "returns the raw number if stdout can't handle fanciness"


def test_concat():
    assert concat({
        'hw1': AssignmentStatus.SUCCESS,
        'hw2': AssignmentStatus.SUCCESS,
    }, 2) == "1 2", "should turn an assignment list into a string"

    assert concat({
        'hw1': AssignmentStatus.SUCCESS,
        'hw2': AssignmentStatus.SUCCESS,
    }, 6) == "1 2 - - - -", "should output hyphens when no assignments are given"

    assert concat({
        'hw1': AssignmentStatus.SUCCESS,
        'hw6': AssignmentStatus.SUCCESS,
    }, 6) == "1 - - - - 6", "should handle missing assignments in between others"

    assert concat({
        'hw10': AssignmentStatus.SUCCESS,
        'hw11': AssignmentStatus.SUCCESS,
    }, 12) == "- - - - - - - - - 10 11 --", "should output two hyphens for two-digit numbers"


def test_columnize():
    student = StudentResult(name='rives',
                            homeworks={
                                'hw1': AssignmentStatus.SUCCESS,
                                'hw2': AssignmentStatus.SUCCESS,
                            },
                            labs={
                                'lab1': AssignmentStatus.SUCCESS,
                            })

    assert columnize(student, 'rives', 2, 1, 1) == "rives  | 1 2 | 1 | -"
    assert columnize(student, 'long_username', 2, 1, 1) == "rives          | 1 2 | 1 | -"
    assert columnize(student, 'rives', 5, 1, 1) == "rives  | 1 2 - - - | 1 | -"
    assert columnize(student, 'rives', 2, 5, 1) == "rives  | 1 2 | 1 - - - - | -"

    student2 = StudentResult(name='rives',
                             unmerged_branches=['branch'],
                             homeworks={
                                 'hw1': AssignmentStatus.SUCCESS,
                                 'hw2': AssignmentStatus.SUCCESS,
                             },
                             labs={
                                 'lab1': AssignmentStatus.SUCCESS,
                             })

    assert columnize(student2, 'rives', 2, 1, 1) == "\033[1mrives\033[0m  | 1 2 | 1 | -"

    student3 = StudentResult(name='rives',
                             error='an error occurred')

    assert columnize(student3, 'rives', 2, 1, 1) == "{username}  | {error}".format(username=student3.name,
                                                                                   error=student3.error)


def test_get_nums():
    assert get_nums([
        StudentResult(name='rives',
                      homeworks={
                          'hw1': AssignmentStatus.SUCCESS,
                          'hw2': AssignmentStatus.SUCCESS,
                      },
                      labs={
                          'lab1': AssignmentStatus.SUCCESS,
                      }),
    ]) == (2, 1, 0)

    assert get_nums([
        StudentResult(name='rives',
                      homeworks={
                          'hw1': AssignmentStatus.SUCCESS,
                          'hw2': AssignmentStatus.SUCCESS,
                      },
                      labs={
                          'lab1': AssignmentStatus.SUCCESS,
                      }),
        StudentResult(name='rives',
                      homeworks={
                          'hw8': AssignmentStatus.SUCCESS,
                          'hw9': AssignmentStatus.SUCCESS,
                      },
                      labs={
                          'lab10': AssignmentStatus.SUCCESS,
                      }),
    ]) == (9, 10, 0)

    assert get_nums([
        StudentResult(name='student',
                      homeworks={},
                      labs={}),
    ]) == (0, 0, 0)

    assert get_nums([
        StudentResult(name='student',
                      homeworks={
                          'hw1': AssignmentStatus.SUCCESS,
                      })
    ]) == (1, 0, 0)

    assert get_nums([
        StudentResult(name='student',
                      labs={
                          'lab1': AssignmentStatus.SUCCESS,
                      })
    ]) == (0, 1, 0)


def test_sort_by_hw_count():  # TODO: Update
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


def test_sort_by_username():  # TODO: Update
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
        StudentResult(name='rives3',
                      homeworks={
                          'hw1': AssignmentStatus.SUCCESS,
                          'hw2': AssignmentStatus.SUCCESS,
                          'hw3': AssignmentStatus.SUCCESS,
                          'hw4': AssignmentStatus.SUCCESS,
                      }),
        StudentResult(name='rives2',
                      homeworks={
                          'hw1': AssignmentStatus.SUCCESS,
                          'hw2': AssignmentStatus.SUCCESS,
                          'hw3': AssignmentStatus.SUCCESS,
                      }),
        StudentResult(name='rives1',
                      homeworks={
                          'hw1': AssignmentStatus.SUCCESS,
                          'hw2': AssignmentStatus.SUCCESS,
                      },
                      labs={
                          'lab1': AssignmentStatus.SUCCESS,
                          'lab2': AssignmentStatus.SUCCESS,
                      },
                      worksheets={
                          'ws1': AssignmentStatus.SUCCESS
                      }),
    ]

    assert tabulate(students) == dedent("""
    USER    | 1 2 3 4 | 1 2 | 1
    --------+---------+-----+--
    rives1  | 1 2 - - | 1 2 | 1
    rives2  | 1 2 3 - | - - | -
    rives3  | 1 2 3 4 | - - | -
    """).strip()

    assert tabulate(students, sort_by='count') == dedent("""
    USER    | 1 2 3 4 | 1 2 | 1
    --------+---------+-----+--
    rives3  | 1 2 3 4 | - - | -
    rives2  | 1 2 3 - | - - | -
    rives1  | 1 2 - - | 1 2 | 1
    """).strip()
