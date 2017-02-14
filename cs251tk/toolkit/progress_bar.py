import sys
from shutil import get_terminal_size

CHAR = '·' if sys.stderr.encoding == 'UTF-8' else '='


def progress_bar(size, current, message=''):
    cols, _ = get_terminal_size()

    filled = [CHAR for i in range(current)]
    empty = [' ' for i in range(size - current)]
    bar = ''.join(filled + empty)

    line = '[{}] {}'.format(bar, message)
    spacers = ' ' * (cols - len(line))

    result = line + spacers
    result = result[:cols]
    print('\r' + result, end='', file=sys.stderr)
