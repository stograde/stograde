#!/usr/bin/env python3
from .termcolor import colored
from sys import stdout

unicode = stdout.encoding == 'UTF-8'
# unicode = False
COL = '│' if unicode else '|'
ROW = '─' if unicode else '-'
JOIN = '┼' if unicode else '-'
MISSING = '─' if unicode else '-'


def pad(string, index):
    padding_char = string if string == MISSING else ' '
    return string.ljust(len(str(index)), padding_char)


def symbol(assignment):
    if assignment['status'] == 'success':
        return str(assignment['number'])
    elif assignment['status'] == 'partial':
        return str(assignment['number'])
        # return colored(str(assignment['number']), 'red', attrs={'bold': True})
    return MISSING


def concat(lst, toNum):
    nums = {item['number']: item for item in lst}
    lst = [pad(symbol(nums[idx]), idx)
           if idx in nums
           else pad('-', idx)
           for idx in range(1, toNum+1)]
    return ' '.join(lst)


def find_columns(num):
    return ' '.join([str(i) for i in range(1, num+1)])


def pluck(lst, attr):
    return [it[attr] for it in lst]


def columnize(students, sort_by):
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

    if sort_by == 'homework':
        def sorter(user):
            return sum([1 if hw['status'] == 'complete' else 0 for hw in user['homework']])
        shouldReverse = True
    else:
        def sorter(user):
            return user['username']
        shouldReverse = False

    lines = []
    for user in sorted(students, reverse=shouldReverse, key=sorter):
        name = '{0:<{1}}'.format(user['username'], len(longest_user))

        if user.get('unmerged_branches', False):
            name = colored(name, attrs={'bold': True})

        homework_row = concat(user['homeworks'], max_hwk_num)
        lab_row = concat(user['labs'], max_lab_num)

        if 'error' in user:
            lines.append('{name}  {sep} {err}'.format(
                name=name,
                sep=sep,
                err=user['error']))
            continue

        line = '{name}  {sep} {hws} {sep} {labs}'.format(
            name=name,
            hws=homework_row,
            labs=lab_row,
            sep=COL)

        lines.append(line)

    return '\n'.join([header, border, '\n'.join(lines)])
