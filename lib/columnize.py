'''Make a nice table from the student results'''
from sys import stdout
from .termcolor import colored
from .helpers import pluck

UNICODE = stdout.encoding == 'UTF-8' and stdout.isatty()
# unicode = False
COL = '│' if UNICODE else '|'
ROW = '─' if UNICODE else '-'
JOIN = '┼' if UNICODE else '-'
MISSING = '─' if UNICODE else '-'


def pad(string, index):
    '''Pad a string to the width of the stringified number'''
    padding_char = string if string == MISSING else ' '
    return string.ljust(len(str(index)), padding_char)


def symbol(assignment):
    '''Turn an assignment status into the symbol for the table'''
    if assignment['status'] == 'success':
        return str(assignment['number'])
    elif assignment['status'] == 'partial':
        return str(assignment['number'])
        # return colored(str(assignment['number']), 'red', attrs={'bold': True})
    return MISSING


def concat(lst, to_num):
    '''Create the informative row of data for a list of assignment statuses'''
    nums = {item['number']: item for item in lst}
    lst = [pad(symbol(nums[idx]), idx)
           if idx in nums
           else pad('-', idx)
           for idx in range(1, to_num+1)]
    return ' '.join(lst)


def find_columns(num):
    '''Build the table headings for the assignment sections'''
    return ' '.join([str(i) for i in range(1, num+1)])


def columnize(student, longest_user, max_hwk_num, max_lab_num):
    '''Build the data for each row of the information table'''
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


def tabulate(students, sort_by):
    '''Actually build the table'''
    max_hwk_num = max([max(pluck(s['homeworks'], 'number')) for s in students])
    max_lab_num = max([max(pluck(s['labs'], 'number')) for s in students])

    # be sure that the longest username will be at least 4 chars
    usernames = [user['username'] for user in students] + ['USER']
    longest_user = max(usernames, key=len)

    header_hw_nums = find_columns(max_hwk_num)
    header_lab_nums = find_columns(max_lab_num)
    header = '{name:<{namesize}}  {sep} {hwnums} {sep} {labnums}'.format(
        name='USER',
        namesize=len(longest_user),
        hwnums=header_hw_nums,
        labnums=header_lab_nums,
        sep=COL)

    border = ''.join([
        ''.ljust(len(longest_user) + 2, ROW),
        JOIN,
        ''.ljust(len(header_hw_nums) + 2, ROW),
        JOIN,
        ''.ljust(len(header_lab_nums) + 1, ROW),
    ])

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

    table = [header, border] + lines
    return '\n'.join(table)
