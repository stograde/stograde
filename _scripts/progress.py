import shutil
from sys import stderr
from .run_command import run

def progress(size, current, message=''):
    # rows, cols = [int(val) for val in run('stty sane size'.split(), status=False).split()]
    cols, rows = shutil.get_terminal_size()

    if message:
        message = ' (' + message + ')'

    FILLED = ['·' for i in range(current)]
    EMPTY  = [' ' for i in range(size - current)]
    BAR = ''.join(FILLED + EMPTY)

    line = '[%s] %s' % (BAR, message)
    spacers = ' ' * (cols - len(line))
    print(line + spacers, end='\r', file=stderr)


if __name__ == '__main__':
    from time import sleep

    # run('tput civis'.split())   # invisible
    size = 10
    for i in range(size + 1):
        progress(size, i, ('a' * size)[:-i] + ' ' + str(i) + ' ' + str(size))
        sleep(1)
