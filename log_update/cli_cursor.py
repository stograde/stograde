from sys import stdout
from .restore_cursor import restore_cursor

hidden = False


def show_cursor():
    global hidden
    hidden = False
    stdout.write('\u001b[?25h')


def hide_cursor():
    restore_cursor()
    global hidden
    hidden = True
    stdout.write('\u001b[?25l')


def toggle_cursor(force=None):
    if force is not None:
        hidden = force

    if hidden:
        show_cursor()
    else:
        hide_cursor()
