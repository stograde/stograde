#!/usr/bin/env python3
from sys import stderr
from shutil import get_terminal_size


def progress(size, current, message=''):
    cols, rows = get_terminal_size()

    FILLED = ['·' for i in range(current)]
    EMPTY = [' ' for i in range(size - current)]
    BAR = ''.join(FILLED + EMPTY)

    line = '[{}] {}'.format(BAR, message)
    spacers = ' ' * (cols - len(line))

    result = line + spacers
    result = result[:cols]
    print(result, end='\r', file=stderr)


if __name__ == '__main__':
    from time import sleep

    size = 10
    for i in range(size + 1):
        progress(size, i, ('a' * size)[:-i] + ' ' + str(i) + ' ' + str(size))
        sleep(1)
