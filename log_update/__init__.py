from sys import stdout, stderr
from .ansi_escapes import erase_lines
from .cli_cursor import show_cursor, hide_cursor
from .spinner import spinner


def create(stream):
    def render(*args):
        hide_cursor()
        out = ' '.join(args) + '\n'
        stream.write(erase_lines(render.prev_line_count) + out)
        render.prev_line_count = len(out.split('\n'))

    def clear():
        stream.write(erase_lines(render.prev_line_count))
        render.prev_line_count = 0

    def done():
        render.prev_line_count = 0
        show_cursor()

    render.prev_line_count = 0
    render.clear = clear
    render.done = done

    return render


stdout = create(stdout)
stderr = create(stderr)
