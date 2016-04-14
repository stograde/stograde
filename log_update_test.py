import log_update
from textwrap import dedent
import time
from lib import flatten

log = log_update.stdout

MISSING = '__MISSING__'
RECORDING = '__RECORDING__'
PULLING = '__PULLING__'
GOOD = '__GOOD__'
PARTIAL = '__PARTIAL__'
MISSING = '__MISSING__'

data = [
    {
        'user': 'rives',
        'homework': {
            1: GOOD,
            2: GOOD,
            3: PARTIAL,
            4: RECORDING,
        },
        'labs': {},
    },
    {
        'user': 'carson5',
        'unmerged_branches': True,
        'homework': {
            1: GOOD,
            2: MISSING,
            3: GOOD,
            4: MISSING,
            5: RECORDING,
            6: RECORDING,
        },
        'labs': {
            1: GOOD,
        },
    },
]

alt_data = [
    {
        'user': 'rives',
        'homework': {
            1: GOOD,
            2: GOOD,
            3: PARTIAL,
            4: GOOD,
        },
        'labs': {},
    },
    {
        'user': 'carson5',
        'unmerged_branches': True,
        'homework': {
            1: GOOD,
            2: MISSING,
            3: GOOD,
            4: MISSING,
            5: PARTIAL,
            6: GOOD,
        },
        'labs': {
            1: GOOD,
        },
    },
]


def format_entry(key, value, opts):
    if value == GOOD:
        return str(key)
    elif value == RECORDING:
        return opts['spinner']
    elif value == PARTIAL:
        return '~'
    elif value == MISSING:
        return '-'
    else:
        return str(value)


def parts(dict, opts):
    return ' '.join([format_entry(k, v, opts) for k, v in dict.items()])


def format_name_column(contents, size):
    return '{contents:<{size}}'.format(contents=contents, size=size)


def row(**kwargs):
    kwargs['hw'] = parts(kwargs['homework'], kwargs)
    kwargs['lb'] = parts(kwargs['labs'], kwargs)

    name = format_name_column(kwargs['user'], kwargs['longest_user'])
    pads = format_name_column(' ', kwargs['longest_user'])

    line1 = name + ' │ {hw}'.format_map(kwargs)
    line2 = pads + ' │ {lb}'.format_map(kwargs)

    if not kwargs['labs']:
        return line1
    return line1 + '\n' + line2


def longest(lst):
    return max(lst, key=lambda item: len(item))


def homework_lab_count(data):
    hw = flatten([list(d['homework'].keys()) for d in data])
    labs = flatten([list(d['labs'].keys()) for d in data])
    return max(set(list(hw) + list(labs)))


def generate_header(data, opts):
    count = homework_lab_count(data)
    nums = ' '.join([str(i) for i in range(1, count+1)])
    header = '{} │ {}'.format(format_name_column('STUDENT', opts['longest_user']), nums)
    border = ''.join(['┼' if ch == '│' else '─' for ch in header])
    return header + '\n' + border


def table(data):
    usernames = [u['user'] for u in data]
    longest_user = len(longest(usernames + ['STUDENT']))

    spinner = log_update.spinner()
    opts = {'longest_user': longest_user}
    header = generate_header(data, opts)

    def inner(inner_data=data):
        opts['spinner'] = spinner()
        return header + '\n' + '\n'.join([row(**opts, **data_row) for data_row in inner_data])

    return inner


t = table(data)
for i in range(50):
    log(t())
    time.sleep(80 / 1000)
log(t(alt_data))
