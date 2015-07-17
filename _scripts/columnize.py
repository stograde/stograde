#!/usr/bin/env python3

from functools import reduce
import re
import sys

rex = re.compile(r'(\d+)$')


def getNumber(string):
    maybe_match = rex.search(string)
    return int(maybe_match.group(1)) if maybe_match else 0


def sum(lst):
    return reduce(lambda acc, item: acc + item, lst, 0)


def make_list(data):
    numbered = [getNumber(item) for item in data.split()]
    return [idx if idx in numbered else False for idx in range(1, max(numbered) + 1)]


success = '✓'
missing = '-'


def pad(string, size):
    return '{0:>{1}} '.format(string, len(str(size)))


def concat(lst, max):
    return [pad(str(idx), idx) if idx in lst else pad(missing, idx) for idx in range(1, max+1)]


def find_columns(max):
        return ' '.join([str(i) for i in range(1, max+1)])


def main(inputData):
    users = []

    max_hwk = 0
    max_lab = 0
    for line in inputData:
        line = line.strip().split('\t')
        user = line[0].strip()

        hwks = make_list(line[1].strip()) if len(line) > 1 else False
        labs = make_list(line[2].strip() if len(line) >= 3 else '0') if len(line) > 2 else False

        if hwks:
            max_hwk_local = max(hwks)
            max_hwk = max_hwk_local if max_hwk_local > max_hwk else max_hwk

        if labs:
            max_lab_local = max(labs)
            max_lab = max_lab_local if max_lab_local > max_lab else max_lab

        users.append({
            'username': user,
            'homework': hwks or [],
            'labs': labs or []
        })

    longest_user = reduce(
        lambda longest, curr: curr if len(curr) > len(longest) else longest,
        map(lambda u: u['username'], users),
        'USER')

    header = '{0:<{1}}  | {2} | {3}'.format(
        'USER', len(longest_user),
        find_columns(max_hwk),
        find_columns(max_lab))

    border = ''.ljust(len(header), '-')

    lines = ''
    # for user in sorted(users, reverse=True, key=lambda user: sum([1 if hw else 0 for hw in user['homework']])):
    for user in sorted(users, key=lambda user: user['username']):
        name = '{0:<{1}}'.format(user['username'], len(longest_user))

        homework = concat(user['homework'], max_hwk)
        lab = concat(user['labs'], max_lab)

        line = '{0}  | {1:<{2}}| {3:<{4}}'.format(
            name,
            ''.join(homework), max_hwk * len('' + str(max_hwk)),
            ''.join(lab), max_lab * len('' + str(max_lab)))

        lines += line + '\n'

    return '\n'.join([header, border, lines])


if __name__ == '__main__':
    print(main(sys.stdin))
