from .run_once import run_once
from sys import stdout


@run_once
def __restore_cursor():
    stdout.write('\u001b[?25h')


def restore_cursor():
    import atexit
    atexit.register(__restore_cursor)
