from shutil import get_terminal_size
from unittest import mock

from stograde.toolkit.progress_bar import make_progress_bar


def test_make_progress_bar(capsys):
    make_progress_bar(['student1', 'student2'])

    _, err = capsys.readouterr()

    cols, _ = get_terminal_size()
    spacers = ' ' * (cols - len('[  ] student1, student2'))

    assert err == '\r[  ] student1, student2' + spacers


@mock.patch('stograde.toolkit.progress_bar.CHAR', '=')
def test_make_progress_bar_increment(capsys):
    increment = make_progress_bar(['student1', 'student2'])
    increment('student1')

    _, err = capsys.readouterr()

    cols, _ = get_terminal_size()
    spacers = ' ' * (cols - len('[  ] student1, student2'))
    spacers2 = ' ' * (cols - len('[  ] student2'))

    assert err == '\r[  ] student1, student2' + spacers + '\r[= ] student2' + spacers2


def test_make_progress_bar_no_bar(capsys):
    make_progress_bar(['student1', 'student2'], no_progress_bar=True)

    _, err = capsys.readouterr()

    assert err == ''
