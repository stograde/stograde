#!/usr/bin/env python3

from functools import reduce
import re, sys

rex = re.compile(r'(\d+)$')

def getNumber(string):
	maybe_match = rex.search(string)
	return int(maybe_match.group(1)) if maybe_match else 0

def sum(lst):
	return reduce(lambda acc, item: acc + item, lst, 0)

def main(inputData):
	users = []

	max_hwk = 0
	max_lab = 0
	for line in inputData:
		line = line.strip().split('\t')
		user = line[0].strip()

		if len(line) > 1:
			hwks = line[1].strip()
			hwks = [getNumber(hw) for hw in hwks.split()]
			hwks = [idx if idx in hwks else False for idx in range(1, max(hwks) + 1)]
		else:
			hwks = False

		if len(line) > 2:
			labs = line[2].strip() if len(line) >= 3 else '0'
			labs = [getNumber(lab) for lab in labs.split()]
			labs = [idx if idx in labs else False for idx in range(1, max(labs) + 1)]
		else:
			labs = False

		if hwks:
			max_hwk_local = max(hwks)
			max_hwk = max_hwk_local if max_hwk_local > max_hwk else max_hwk

		if labs:
			max_lab_local = max(labs)
			max_lab = max_lab_local if max_lab_local > max_lab else max_lab

		users.append({'username': user, 'homework': hwks or [], 'labs': labs or []})

	longest_user = reduce(
		lambda longest, current: current if len(current) > len(longest) else longest,
		map(lambda u: u['username'], users),
		'USER')

	find_columns = lambda max: '  '.join(map(str, range(1, max+1)))

	header = '{0:<{1}}  |  {2}  |  {3}'.format(
		'USER', len(longest_user),
		find_columns(max_hwk),
		find_columns(max_lab))

	border = ''.ljust(len(header), '-')

	success = '✓'
	missing = '-'

	pad    = lambda string, size: '{0:>{1}}  '.format(string, len(str(size)))
	concat = lambda lst, max: [pad(str(idx), idx) if idx in lst else pad(missing, idx) for idx in range(1, max+1)]

	lines = ''
	# for user in sorted(users, reverse=True, key=lambda user: sum([1 if hw else 0 for hw in user['homework']])):
	for user in sorted(users, key=lambda user: user['username']):
		name = '{0:<{1}}'.format(user['username'], len(longest_user))

		homework = concat(user['homework'], max_hwk)
		lab      = concat(user['labs'],     max_lab)

		line = ('{0}  |  {1:<{2}}|  {3:<{4}}'.format(name,
			''.join(homework), max_hwk * len(' ' + str(max_hwk)),
			''.join(lab),      max_lab * len(' ' + str(max_lab))))

		lines += line + '\n'


	return '\n'.join([header, border, lines])


if __name__ == '__main__':
	print(main(sys.stdin))
