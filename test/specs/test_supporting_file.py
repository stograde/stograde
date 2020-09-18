from stograde.specs.supporting_file import create_supporting_file


def test_create_supporting_file_dict():
    new_supporting = create_supporting_file({
        'file': 'support_file1.txt',
    })

    assert new_supporting.file_name == 'support_file1.txt'
    assert new_supporting.destination == 'support_file1.txt'


def test_create_supporting_file_dict_with_destination():
    new_supporting = create_supporting_file({
        'file': 'support_file2.txt',
        'destination': 'support_file3.txt'
    })

    assert new_supporting.file_name == 'support_file2.txt'
    assert new_supporting.destination == 'support_file3.txt'


def test_create_supporting_file_bad_dict():
    try:
        create_supporting_file({
            'not_the_right_key': 'some value',
        })
    except AssertionError:
        pass


def test_create_supporting_file_list():
    new_supporting = create_supporting_file(['support_file4.txt'])

    assert new_supporting.file_name == 'support_file4.txt'
    assert new_supporting.destination == 'support_file4.txt'


def test_create_supporting_file_list_with_destination():
    new_supporting = create_supporting_file(['support_file5.txt', 'support_file6.txt'])

    assert new_supporting.file_name == 'support_file5.txt'
    assert new_supporting.destination == 'support_file6.txt'


def test_create_supporting_file_str():
    new_supporting = create_supporting_file('support_file7.txt')

    assert new_supporting.file_name == 'support_file7.txt'
    assert new_supporting.destination == 'support_file7.txt'


def test_create_supporting_file_bad_type():
    try:
        # noinspection PyTypeChecker
        create_supporting_file(15)
    except TypeError:
        pass
