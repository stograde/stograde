ESC = '\u001b['

cursor_left = ESC + '1000D'
cursor_save_position = ESC + 's'
cursor_restore_position = ESC + 'u'
cursor_get_position = ESC + '6n'
cursor_next_line = ESC + 'E'
cursor_prev_line = ESC + 'F'
cursor_hide = ESC + '?25l'
cursor_show = ESC + '?25h'

erase_end_line = ESC + 'K'
erase_start_line = ESC + '1K'
erase_line = ESC + '2K'
erase_down = ESC + 'J'
erase_up = ESC + '1J'
erase_screen = ESC + '2J'
scroll_up = ESC + 'S'
scroll_down = ESC + 'T'

clear_screen = '\u001bc'
beep = '\u0007'


def cursor_to(x=None, y=None):
    if x is None and y is None:
        return ESC + 'H'

    elif x and y is None:
        return ESC + str(x + 1) + 'G'

    return ESC + str(y + 1) + str(x + 1) + 'H'


def cursor_move(x, y):
    ret = ''

    if x < 0:
        ret += ESC + str(-x) + 'D'
    elif x > 0:
        ret += ESC + str(x) + 'C'

    if y < 0:
        ret += ESC + str(-y) + 'A'
    elif y > 0:
        ret += ESC + str(y) + 'B'

    return ret


def cursor_up(count=1):
    return ESC + str(count) + 'A'


def cursor_down(count=1):
    return ESC + str(count) + 'B'


def cursor_forward(count=1):
    return ESC + str(count) + 'C'


def cursor_backward(count=1):
    return ESC + str(count) + 'D'


def erase_lines(count):
    clear = ''
    for i in range(0, count):
        clear += cursor_left + erase_end_line + (cursor_up() if i < count - 1 else '')
    return clear
