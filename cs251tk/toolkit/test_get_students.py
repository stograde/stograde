from textwrap import dedent
from pyfakefs import fake_filesystem
from collections import Mapping
from .get_students import get_students


def write_students_file(fs, students):
    fs.CreateFile('./students.txt')
    with open('./students.txt', 'w', encoding='utf-8') as outfile:
        outfile.write(dedent(students).strip())


def test_get_students_single_name(fs):
    write_students_file(fs, 'rives')

    # verify that we got a dict
    assert isinstance(get_students(), Mapping)

    # this dict should have a 'my' section
    assert 'my' in get_students()

    # and the "my" section should include one username
    assert get_students()['my'] == ['rives']


def test_get_students_multiple_names(fs):
    write_students_file(fs, '''
    rives
    piersonv
    magnusow
    ''')

    # verify that we got a dict
    assert isinstance(get_students(), Mapping)

    # this dict should have a 'my' section
    assert 'my' in get_students()

    # and the "my" section should include one username
    assert get_students()['my'] == ['rives', 'piersonv', 'magnusow']


def test_get_students_single_section(fs):
    write_students_file(fs, '''
    [alt]
    rye
    ''')

    assert 'alt' in get_students()
    assert get_students()['alt'] == ['rye']


def test_get_students_multiple_sections(fs):
    write_students_file(fs, '''
    [my]
    rives
    piersonv
    magnusow

    [section-a]
    piersonv

    [section-b]
    magnusow
    ''')

    assert 'my' in get_students()
    assert 'section-a' in get_students()
    assert 'section-b' in get_students()

    assert get_students()['my'] == ['rives', 'piersonv', 'magnusow']
    assert get_students()['section-a'] == ['piersonv']
    assert get_students()['section-b'] == ['magnusow']


def test_get_students_missing_file(fs):
    os_module = fake_filesystem.FakeOsModule(fs)
    assert os_module.path.exists('./students.txt') == False
    assert get_students() == {'my': []}
