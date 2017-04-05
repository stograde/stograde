"""Make a nice table from the student results"""
import re
from sys import stdout
from termcolor import colored

COL = '|'
ROW = '-'
JOIN = '+'
MISSING = '-'
ANSI_ESCAPE = re.compile(r'\x1b[^m]*m')


def sort_by_hw_count(user):
    """Sort students by the number of completed homeworks"""
    return sum([1 if hw['status'] == 'success' else 0 for hw in user['homeworks']])


def sort_by_username(user):
    """Sort students by their username"""
    return user['username']


def asciiify(table):
    """Take a flashy unicode table and render it with ASCII-only chars"""
    return ANSI_ESCAPE.sub('', table)


def pad(string, index):
    """Pad a string to the width of the stringified number"""
    padding_char = string if string == MISSING else ' '
    return string.ljust(len(str(index)), padding_char)


def symbol(assignment, highlight_partials=False):
    """Turn an assignment status into the symbol for the table"""
    if assignment['status'] == 'success':
        return str(assignment['number'])
    elif assignment['status'] == 'partial':
        retval = str(assignment['number'])
        if highlight_partials:
            return colored(retval, 'red', attrs={'bold': True})
        return retval
    return MISSING


def concat(lst, to_num, highlight_partials=False):
    """Create the informative row of data for a list of assignment statuses"""
    nums = {item['number']: item for item in lst}
    lst = [pad(symbol(nums[idx], highlight_partials), idx)
           if idx in nums
           else pad('-', idx)
           for idx in range(1, to_num + 1)]
    return ' '.join(lst)


def find_columns(num):
    """Build the table headings for the assignment sections"""
    return ' '.join([str(i) for i in range(1, num + 1)])


def columnize(student, longest_user, max_hwk_num, max_lab_num, highlight_partials=False):
    """Build the data for each row of the information table"""
    name = '{0:<{1}}'.format(student['username'], len(longest_user))

    if student.get('unmerged_branches', False):
        name = colored(name, attrs={'bold': True})

    homework_row = concat(student.get('homeworks', []), max_hwk_num, highlight_partials)
    lab_row = concat(student.get('labs', []), max_lab_num, highlight_partials)

    if 'error' in student:
        return '{name}  {sep} {err}'.format(
            name=name,
            sep=COL,
            err=student['error'])

    return '{name}  {sep} {hws} {sep} {labs}'.format(
        name=name,
        hws=homework_row,
        labs=lab_row,
        sep=COL)


def get_nums(students):
    """Given a list of students, return the higest hw and lab number among them"""
    homework_nums = [hw['number'] for s in students for hw in s.get('homeworks', [])]
    lab_nums = [lab['number'] for s in students for lab in s.get('labs', [])]

    max_hwk_num = max(homework_nums, default=0)
    max_lab_num = max(lab_nums, default=0)

    return max_hwk_num, max_lab_num


def tabulate(students, sort_by='name', highlight_partials=False):
    """Actually build the table"""

    # be sure that the longest username will be at least 4 chars
    usernames = [user['username'] for user in students] + ['USER']
    longest_user = max(usernames, key=len)

    # build the header row of the table
    max_hwk_num, max_lab_num = get_nums(students)
    header_hw_nums = find_columns(max_hwk_num)
    header_lab_nums = find_columns(max_lab_num)
    header = '{name:<{namesize}}  {sep} {hwnums} {sep} {labnums}'.format(
        name='USER',
        namesize=len(longest_user),
        hwnums=header_hw_nums,
        labnums=header_lab_nums,
        sep=COL)

    # build the header's bottom border
    border = ''.join([
        ''.ljust(len(longest_user) + 2, ROW),
        JOIN,
        ''.ljust(len(header_hw_nums) + 2, ROW),
        JOIN,
        ''.ljust(len(header_lab_nums) + 1, ROW),
    ])

    # build the table body
    if sort_by == 'count':
        sorter = sort_by_hw_count
        should_reverse = True
    else:
        sorter = sort_by_username
        should_reverse = False

    lines = [columnize(student, longest_user, max_hwk_num, max_lab_num, highlight_partials=highlight_partials)
             for student in sorted(students, reverse=should_reverse, key=sorter)]

    # and make the table to return
    table = [header, border] + lines
    return '\n'.join(table)
