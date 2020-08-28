from shutil import get_terminal_size
import sys
from typing import List, Callable

CHAR = '·' if sys.stderr.encoding == 'UTF-8' else '='


def progress_bar(size: int, current: int, message: str = ''):
    cols, _ = get_terminal_size()

    filled = [CHAR for i in range(current)]
    empty = [' ' for i in range(size - current)]
    bar = ''.join(filled + empty)

    line = '[{}] {}'.format(bar, message)
    spacers = ' ' * (cols - len(line))

    result = line + spacers
    result = result[:cols]
    print('\r' + result, end='', file=sys.stderr)


def make_progress_bar(students: List[str], no_progress_bar: bool = False) -> Callable[[str], None]:
    if no_progress_bar:
        return lambda _: None

    size = len(students)
    remaining = set(students)
    invocation_count = 0

    def increment(username: str):
        nonlocal remaining
        nonlocal invocation_count
        remaining.remove(username)
        invocation_count += 1
        msg = ', '.join(sorted(remaining))
        progress_bar(size, invocation_count, message=msg)

    msg = ', '.join(sorted(remaining))
    progress_bar(size, invocation_count, message=msg)
    return increment
