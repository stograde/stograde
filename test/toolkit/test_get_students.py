from textwrap import dedent
from pyfakefs import fake_filesystem
from stograde.toolkit.get_students import get_students, get_students_from_file, filter_sections


def write_students_file(fs, students):
    fs.create_file('./students.txt')
    with open('./students.txt', 'w', encoding='utf-8') as outfile:
        outfile.write(dedent(students).strip())


def test_get_students_with_cmd_line():
    assert get_students({'sections': ['section-a'],
                         'students': [['student1'],
                                      ['narvae1', 'rives']]}) == ['narvae1', 'rives', 'student1']


def test_get_students_with_sections(fs):
    write_students_file(fs, '''
    [section-a]
    piersonv

    [section-b]
    magnusow

    [section-c]
    narvae1
    ''')

    assert get_students({'sections': ['section-c'],
                         'students': []}) == ['narvae1']


def test_get_students_without_sections(fs):
    write_students_file(fs, '''
    rives

    [section-a]
    piersonv

    [section-b]
    magnusow

    [section-c]
    narvae1
    ''')

    assert get_students({'sections': [],
                         'students': []}) == ['magnusow', 'narvae1', 'piersonv', 'rives']


def test_get_students_from_file_single_name(fs):
    write_students_file(fs, 'rives')

    # verify that we got a dict
    assert isinstance(get_students_from_file(), dict)

    # this dict should have a 'no_section' section
    assert 'no_section' in get_students_from_file()

    # and the 'no_section' section should include one username
    assert get_students_from_file()['no_section'] == ['rives']


def test_get_students_from_file_multiple_names(fs):
    write_students_file(fs, '''
    rives
    piersonv
    magnusow
    ''')

    # verify that we got a dict
    assert isinstance(get_students_from_file(), dict)

    # this dict should have a 'no_section' section
    assert 'no_section' in get_students_from_file()

    # and the 'no_section' section should include one username
    assert get_students_from_file()['no_section'] == ['rives', 'piersonv', 'magnusow']


def test_get_students_from_file_single_section(fs):
    write_students_file(fs, '''
    [alt]
    rye
    ''')

    assert 'alt' in get_students_from_file()
    assert get_students_from_file()['alt'] == ['rye']


def test_get_students_from_file_multiple_sections(fs):
    write_students_file(fs, '''
    rives
    piersonv
    magnusow

    [section-a]
    piersonv

    [section-b]
    magnusow
    ''')

    assert 'no_section' in get_students_from_file()
    assert 'section-a' in get_students_from_file()
    assert 'section-b' in get_students_from_file()

    assert get_students_from_file()['no_section'] == ['rives', 'piersonv', 'magnusow']
    assert get_students_from_file()['section-a'] == ['piersonv']
    assert get_students_from_file()['section-b'] == ['magnusow']


def test_get_students_from_file_missing_file(fs):
    os_module = fake_filesystem.FakeOsModule(fs)
    assert not os_module.path.exists('./students.txt')
    assert get_students_from_file() == {'no_section': []}


def test_filter_sections_present():
    sections = {'a': ['rives'],
                'b': ['narvae1']}

    assert filter_sections(sections, ['a']) == {'a': ['rives']}


def test_filter_sections_prefixed():
    sections = {'section-a': ['rives'],
                'b': ['narvae1']}

    assert filter_sections(sections, ['a']) == {'a': ['rives']}


def test_filter_sections_absent(caplog):
    sections = {'a': ['rives'],
                'b': ['narvae1']}

    assert filter_sections(sections, ['c']) == {'c': []}

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('Neither section [section-c] nor [c] could be found in ./students.txt', 'WARNING')}
