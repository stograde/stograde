from stograde.specs.file_options import FileOptions
from stograde.specs.spec_file import create_spec_file


def check_file_options_has_defaults(options: FileOptions,
                                    *,
                                    test_compile_optional: bool = True,
                                    test_hide_contents: bool = True,
                                    test_optional: bool = True,
                                    test_timeout: bool = True,
                                    test_truncate_output: bool = True,
                                    test_truncate_contents: bool = True,
                                    test_web_file: bool = True,
                                    ):
    defaults = FileOptions()

    if test_compile_optional:
        assert options.compile_optional == defaults.compile_optional
    if test_hide_contents:
        assert options.hide_contents == defaults.hide_contents
    if test_optional:
        assert options.optional == defaults.optional
    if test_timeout:
        assert options.timeout == defaults.timeout
    if test_truncate_output:
        assert options.truncate_output == defaults.truncate_output
    if test_truncate_contents:
        assert options.truncate_contents == defaults.truncate_contents
    if test_web_file:
        assert options.web_file == defaults.web_file


def test_create_spec_file_no_file_tag():
    try:
        create_spec_file({
            'some_other_key': 5,
        })
    except AssertionError:
        pass


def test_create_spec_file_filename_only():
    new_file = create_spec_file({
        'file': 'test_file1.txt',
    })

    assert new_file.file_name == 'test_file1.txt'
    assert not new_file.compile_commands
    assert not new_file.test_commands
    check_file_options_has_defaults(new_file.options)


def test_create_spec_file_with_commands_str():
    new_file = create_spec_file({
        'file': 'test_file2.txt',
        'commands': 'compile command',
    })

    assert new_file.file_name == 'test_file2.txt'
    assert new_file.compile_commands == ['compile command']
    assert not new_file.test_commands
    check_file_options_has_defaults(new_file.options)


def test_create_spec_file_with_commands_list():
    new_file = create_spec_file({
        'file': 'test_file3.txt',
        'commands': ['compile command', 'other command'],
    })

    assert new_file.file_name == 'test_file3.txt'
    assert new_file.compile_commands == ['compile command', 'other command']
    assert not new_file.test_commands
    check_file_options_has_defaults(new_file.options)


def test_create_spec_file_with_tests_str():
    new_file = create_spec_file({
        'file': 'test_file4.txt',
        'tests': 'test command',
    })

    assert new_file.file_name == 'test_file4.txt'
    assert not new_file.compile_commands
    assert new_file.test_commands == ['test command']
    check_file_options_has_defaults(new_file.options)


def test_create_spec_file_with_tests_list():
    new_file = create_spec_file({
        'file': 'test_file5.txt',
        'tests': ['test command', 'other test command'],
    })

    assert new_file.file_name == 'test_file5.txt'
    assert not new_file.compile_commands
    assert new_file.test_commands == ['test command', 'other test command']
    check_file_options_has_defaults(new_file.options)


def test_create_spec_file_with_compile_optional():
    new_file = create_spec_file({
        'file': 'test_file6.txt',
        'options': {
            'optional_compile': True
        }
    })

    assert new_file.file_name == 'test_file6.txt'
    assert not new_file.compile_commands
    assert not new_file.test_commands
    assert new_file.options.compile_optional is True
    check_file_options_has_defaults(new_file.options,
                                    test_compile_optional=False)


def test_create_spec_file_with_hide_contents():
    new_file = create_spec_file({
        'file': 'test_file7.txt',
        'options': {
            'hide_contents': True
        }
    })

    assert new_file.file_name == 'test_file7.txt'
    assert not new_file.compile_commands
    assert not new_file.test_commands
    assert new_file.options.hide_contents is True
    check_file_options_has_defaults(new_file.options,
                                    test_hide_contents=False)


def test_create_spec_file_with_optional():
    new_file = create_spec_file({
        'file': 'test_file8.txt',
        'options': {
            'optional': True
        }
    })

    assert new_file.file_name == 'test_file8.txt'
    assert not new_file.compile_commands
    assert not new_file.test_commands
    assert new_file.options.optional is True
    check_file_options_has_defaults(new_file.options,
                                    test_optional=False)


def test_create_spec_file_with_timeout():
    new_file = create_spec_file({
        'file': 'test_file9.txt',
        'options': {
            'timeout': 50
        }
    })

    assert new_file.file_name == 'test_file9.txt'
    assert not new_file.compile_commands
    assert not new_file.test_commands
    assert new_file.options.timeout == 50
    check_file_options_has_defaults(new_file.options,
                                    test_timeout=False)


def test_create_spec_file_with_truncate_contents():
    new_file = create_spec_file({
        'file': 'test_file10.txt',
        'options': {
            'truncate_contents': 200
        }
    })

    assert new_file.file_name == 'test_file10.txt'
    assert not new_file.compile_commands
    assert not new_file.test_commands
    assert new_file.options.truncate_contents == 200
    check_file_options_has_defaults(new_file.options,
                                    test_truncate_contents=False)


def test_create_spec_file_with_truncate_output():
    new_file = create_spec_file({
        'file': 'test_file11.txt',
        'options': {
            'truncate_output': 200
        }
    })

    assert new_file.file_name == 'test_file11.txt'
    assert not new_file.compile_commands
    assert not new_file.test_commands
    assert new_file.options.truncate_output == 200
    check_file_options_has_defaults(new_file.options,
                                    test_truncate_output=False)


def test_create_spec_file_with_web_file():
    new_file = create_spec_file({
        'file': 'test_file12.txt',
        'options': {
            'web': True
        }
    })

    assert new_file.file_name == 'test_file12.txt'
    assert not new_file.compile_commands
    assert not new_file.test_commands
    assert new_file.options.web_file is True
    check_file_options_has_defaults(new_file.options,
                                    test_web_file=False)


def test_create_spec_file_with_legacy_list():
    new_file = create_spec_file([
        'test_file13.txt',
        'compile command',
        'other compile command',
        {'truncate_contents': 500},
        {'web': True},
    ])

    assert new_file.file_name == 'test_file13.txt'
    assert new_file.compile_commands == ['compile command', 'other compile command']
    assert not new_file.test_commands
    assert new_file.options.truncate_contents == 500
    assert new_file.options.web_file is True
    check_file_options_has_defaults(new_file.options,
                                    test_truncate_contents=False,
                                    test_web_file=False)


def test_create_spec_file_bad_type():
    try:
        create_spec_file(15)
    except TypeError:
        pass


def test_add_from_tests_list():
    new_file = create_spec_file({
        'file': 'test_file14.txt',
        'tests': ['test command', 'other test command'],
    }).add_from_tests([['test_file14.txt',
                        'yet another test command',
                        'another command',
                        {'not_a_command': True},
                        ],
                       ['not_the_file.txt',
                        'bad command',
                        'another bad command',
                        ],
                       ['test_file14.txt'],  # Testing when name is present but no tests
                       ])

    assert new_file.file_name == 'test_file14.txt'
    assert not new_file.compile_commands
    assert new_file.test_commands == ['test command',
                                      'other test command',
                                      'yet another test command',
                                      'another command']
    check_file_options_has_defaults(new_file.options)


def test_add_from_tests_dict_str():
    new_file = create_spec_file({
        'file': 'test_file15.txt',
        'tests': ['test command', 'other test command'],
    }).add_from_tests([{
        'file': 'test_file15.txt',
        'commands': 'another command'
    }])

    assert new_file.file_name == 'test_file15.txt'
    assert not new_file.compile_commands
    assert new_file.test_commands == ['test command',
                                      'other test command',
                                      'another command']
    check_file_options_has_defaults(new_file.options)


def test_add_from_tests_dict_list():
    new_file = create_spec_file({
        'file': 'test_file16.txt',
        'tests': ['test command', 'other test command'],
    }).add_from_tests([{
        'file': 'test_file16.txt',
        'commands': ['another command', 'more command']
    }])

    assert new_file.file_name == 'test_file16.txt'
    assert not new_file.compile_commands
    assert new_file.test_commands == ['test command',
                                      'other test command',
                                      'another command',
                                      'more command']
    check_file_options_has_defaults(new_file.options)


def test_add_from_tests_bad_type():
    try:
        create_spec_file({
            'file': 'test_file17.txt'
        }).add_from_tests([15])
    except TypeError:
        pass
