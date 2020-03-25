"""Make a nice table from the student results"""
import re
from typing import List, Tuple, Dict

from termcolor import colored

from stograde.process_assignment.assignment_status import AssignmentStatus
from stograde.process_assignment.assignment_type import get_assignment_number, AssignmentType
from stograde.student.student_result import StudentResult

COL = '|'
ROW = '-'
JOIN = '+'
MISSING = '-'
ANSI_ESCAPE = re.compile(r'\x1b[^m]*m')


def sort_by_hw_count(user: StudentResult) -> int:
    """Sort students by the number of completed homeworks"""
    return sum([1 if stat is AssignmentStatus.SUCCESS else 0 for _, stat in user.assignments().items()])


def sort_by_username(user: StudentResult) -> str:
    """Sort students by their username"""
    return user.name


def asciiify(table: str) -> str:
    """Take a flashy unicode table and render it with ASCII-only chars"""
    return ANSI_ESCAPE.sub('', table)


def pad(string: str,
        index: int) -> str:
    """Pad a string to the width of the stringified number"""
    padding_char = string if string == MISSING else ' '
    return string.ljust(len(str(index)), padding_char)


def symbol(assignment: Tuple[int, AssignmentStatus],
           highlight_partials: bool = False) -> str:
    """Turn an assignment status into the symbol for the table"""
    (num, status) = assignment

    if status is AssignmentStatus.SUCCESS:
        return str(num)
    elif status is AssignmentStatus.PARTIAL:
        return_val = str(num)
        if highlight_partials:
            return colored(return_val, 'red', attrs={'bold': True})
        return return_val
    else:
        return MISSING


def concat(assignments: Dict[str, AssignmentStatus],
           to_num: int,
           highlight_partials: bool = False) -> str:
    """Create the informative row of data for a list of assignment statuses"""
    nums = {get_assignment_number(a_id): (get_assignment_number(a_id), stat)
            for a_id, stat in assignments.items()}
    lst = [pad(symbol(nums[idx], highlight_partials), idx)
           if idx in nums
           else pad('-', idx)
           for idx in range(1, to_num + 1)]
    return ' '.join(lst)


def find_columns(num: int) -> str:
    """Build the table headings for the assignment sections"""
    return ' '.join([str(i) for i in range(1, num + 1)])


def columnize(student: StudentResult,
              longest_user: str,
              max_hwk_num: int,
              max_lab_num: int,
              max_wst_num: int,
              highlight_partials: bool = False):
    """Build the data for each row of the information table"""
    name = '{0:<{1}}'.format(student.name, len(longest_user))

    if len(student.unmerged_branches) > 0:
        name = colored(name, attrs={'bold': True})

    homework_row = concat(student.homeworks, max_hwk_num, highlight_partials)
    lab_row = concat(student.labs, max_lab_num, highlight_partials)
    worksheet_row = concat(student.worksheets, max_wst_num, highlight_partials)

    if student.error:
        return '{name}  {sep} {err}'.format(
            name=name,
            sep=COL,
            err=student.error)
    else:
        return '{name}  {sep} {hws} {sep} {labs} {sep} {wkshts}'.format(
            name=name,
            hws=homework_row,
            labs=lab_row,
            wkshts=worksheet_row,
            sep=COL)


def get_nums(students: List[StudentResult]) -> Tuple[int, int, int]:
    """Given a list of students, return the highest hw and lab number among them"""
    homework_nums = [get_assignment_number(hw) for s in students for hw in s.homeworks.keys()]
    lab_nums = [get_assignment_number(lab) for s in students for lab in s.labs.keys()]
    worksheet_nums = [get_assignment_number(ws) for s in students for ws in s.worksheets.keys()]

    max_hwk_num = max(homework_nums, default=0)
    max_lab_num = max(lab_nums, default=0)
    max_worksheet_num = max(worksheet_nums, default=0)

    return max_hwk_num, max_lab_num, max_worksheet_num


def tabulate(student_results: List[StudentResult],
             sort_by: str = 'name',
             highlight_partials: bool = False) -> str:
    """Actually build the table"""

    # be sure that the longest username will be at least 4 chars
    usernames = [user.name for user in student_results] + ['USER']
    longest_user = max(usernames, key=len)

    # build the header row of the table
    max_hwk_num, max_lab_num, max_wst_num = get_nums(student_results)
    header_hw_nums = find_columns(max_hwk_num)
    header_lab_nums = find_columns(max_lab_num)
    header_wst_nums = find_columns(max_wst_num)
    header = '{name:<{namesize}}  {sep} {hwnums} {sep} {labnums} {sep} {wstnums}'.format(
        name='USER',
        namesize=len(longest_user),
        hwnums=header_hw_nums,
        labnums=header_lab_nums,
        wstnums=header_wst_nums,
        sep=COL)

    # build the header's bottom border
    border = ''.join([
        ''.ljust(len(longest_user) + 2, ROW),
        JOIN,
        ''.ljust(len(header_hw_nums) + 2, ROW),
        JOIN,
        ''.ljust(len(header_lab_nums) + 2, ROW),
        JOIN,
        ''.ljust(len(header_wst_nums) + 1, ROW),
    ])

    # build the table body
    # Sorts by sorter2, then by sorter1
    # This works because sorted is "stable", meaning it preserves the original order
    # So sorter1 is the main sort, and any duplicate keys are sorted by sorter2
    if sort_by == 'count':
        sorter1 = sort_by_hw_count
        sorter2 = sort_by_username
        should_reverse = True
    else:
        sorter1 = sort_by_username
        sorter2 = sort_by_hw_count
        should_reverse = False

    lines = [columnize(student, longest_user, max_hwk_num, max_lab_num, max_wst_num,
                       highlight_partials=highlight_partials)
             for student in sorted(sorted(student_results, key=sorter2), reverse=should_reverse, key=sorter1)]

    # and make the table to return
    table = [header, border] + lines
    return '\n'.join(table)
