#!/usr/bin/env python3
from sys import stderr
from shutil import get_terminal_size

CHAR = '·' if stderr.encoding == 'UTF-8' else '='


def progress_bar(size, current, message=''):
    cols, _ = get_terminal_size()

    filled = [CHAR for i in range(current)]
    empty = [' ' for i in range(size - current)]
    bar = ''.join(filled + empty)

    line = '[{}] {}'.format(bar, message)
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
