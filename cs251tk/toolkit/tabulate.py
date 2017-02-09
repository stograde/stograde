"""Make a nice table from the student results"""
import re
from sys import stdout
from termcolor import colored
from logging import warning
from cs251tk.common import flatten

UNICODE = stdout.encoding == 'UTF-8' and stdout.isatty()
# unicode = False
COL = '│' if UNICODE else '|'
ROW = '─' if UNICODE else '-'
JOIN = '┼' if UNICODE else '-'
MISSING = '─' if UNICODE else '-'
HIGHLIGHT_PARTIALS = False
ANSI_ESCAPE = re.compile(r'\x1b[^m]*m')


def asciiify(table):
    table = table.replace('│', '|')
    table = table.replace('─', '-')
    table = table.replace('┼', '-')
    table = table.replace('─', '-')
    table = ANSI_ESCAPE.sub('', table)
    return table


def pad(string, index):
    """Pad a string to the width of the stringified number"""
    padding_char = string if string == MISSING else ' '
    return string.ljust(len(str(index)), padding_char)


def symbol(assignment):
    """Turn an assignment status into the symbol for the table"""
    if assignment['status'] == 'success':
        return str(assignment['number'])
    elif assignment['status'] == 'partial':
        retval = str(assignment['number'])
        if HIGHLIGHT_PARTIALS:
            return colored(retval, 'red', attrs={'bold': True})
        return retval
    return MISSING


def concat(lst, to_num):
    """Create the informative row of data for a list of assignment statuses"""
    nums = {item['number']: item for item in lst}
    lst = [pad(symbol(nums[idx]), idx)
           if idx in nums
           else pad('-', idx)
           for idx in range(1, to_num+1)]
    return ' '.join(lst)


def find_columns(num):
    """Build the table headings for the assignment sections"""
    return ' '.join([str(i) for i in range(1, num+1)])


def columnize(student, longest_user, max_hwk_num, max_lab_num):
    """Build the data for each row of the information table"""
    name = '{0:<{1}}'.format(student['username'], len(longest_user))

    if student.get('unmerged_branches', False):
        name = colored(name, attrs={'bold': True})

    homework_row = concat(student['homeworks'], max_hwk_num)
    lab_row = concat(student['labs'], max_lab_num)

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
    homework_nums = flatten([[hw['number'] for hw in s.get('homeworks', [])] for s in students])
    lab_nums = flatten([[lab['number'] for lab in s.get('labs', [])] for s in students])

    if not homework_nums:
        warning('no homework assignments were given to tabulate')
        warning('from these students:')
        warning(students)
        return 0, 0
    if not lab_nums:
        warning('no labs were given to tabulate')
        warning('from these students:')
        warning(students)
        return 0, 0

    max_hwk_num = max(homework_nums)
    max_lab_num = max(lab_nums)

    return max_hwk_num, max_lab_num


def tabulate(students, sort_by, partials):
    """Actually build the table"""
    global HIGHLIGHT_PARTIALS
    HIGHLIGHT_PARTIALS = partials

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
        def sorter(user):
            return sum([1 if hw['status'] == 'complete' else 0 for hw in user['homework']])
        should_reverse = True
    else:
        def sorter(user):
            return user['username']
        should_reverse = False

    lines = [columnize(student, longest_user, max_hwk_num, max_lab_num)
             for student in sorted(students, reverse=should_reverse, key=sorter)]

    # and make the table to return
    table = [header, border] + lines
    return '\n'.join(table)
