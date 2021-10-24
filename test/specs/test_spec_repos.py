from stograde.specs.spec_repos import format_supported_course_list, github_https_clone_address, \
    github_ssh_clone_address, get_spec_download_url, get_course_from_spec_url, default_course


def test_format_supported_course_list():
    assert format_supported_course_list(', ') == 'SD, HD, ADS, OS, MCA'
    assert format_supported_course_list('/') == 'SD/HD/ADS/OS/MCA'
    assert format_supported_course_list('.') == 'SD.HD.ADS.OS.MCA'
    assert format_supported_course_list('---') == 'SD---HD---ADS---OS---MCA'


def test_github_https_clone_address():
    assert github_https_clone_address('something') == 'https://github.com/stograde/something.git'
    assert github_https_clone_address('something-else') == 'https://github.com/stograde/something-else.git'
    assert github_https_clone_address('') == 'https://github.com/stograde/.git'


def test_github_ssh_clone_address():
    assert github_ssh_clone_address('something') == 'git@github.com:stograde/something.git'
    assert github_ssh_clone_address('something-else') == 'git@github.com:stograde/something-else.git'
    assert github_ssh_clone_address('') == 'git@github.com:stograde/.git'


def test_get_spec_download_url():
    assert get_spec_download_url('SD') == 'https://github.com/stograde/cs251-specs.git'
    assert get_spec_download_url('HD') == 'https://github.com/stograde/cs241-specs.git'
    assert get_spec_download_url('ADS') == 'https://github.com/stograde/cs253-specs.git'
    assert get_spec_download_url('OS') == 'https://github.com/stograde/cs273-specs.git'
    assert get_spec_download_url('MCA') == 'https://github.com/stograde/cs284-specs.git'


def test_get_spec_download_url_error(capsys):
    try:
        get_spec_download_url('BAD')
        raise AssertionError
    except SystemExit:
        pass

    _, err = capsys.readouterr()

    assert err == 'Invalid course: BAD\n'


def test_get_course_from_spec_url(capsys):
    assert get_course_from_spec_url('https://github.com/stograde/cs251-specs.git') == 'SD'
    assert get_course_from_spec_url('git@github.com:stograde/cs251-specs.git') == 'SD'

    assert get_course_from_spec_url('https://github.com/stograde/cs241-specs.git') == 'HD'
    assert get_course_from_spec_url('git@github.com:stograde/cs241-specs.git') == 'HD'

    assert get_course_from_spec_url('https://github.com/stograde/cs253-specs.git') == 'ADS'
    assert get_course_from_spec_url('git@github.com:stograde/cs253-specs.git') == 'ADS'

    assert get_course_from_spec_url('https://github.com/stograde/cs273-specs.git') == 'OS'
    assert get_course_from_spec_url('git@github.com:stograde/cs273-specs.git') == 'OS'

    assert get_course_from_spec_url('https://github.com/stograde/cs284-specs.git') == 'MCA'
    assert get_course_from_spec_url('git@github.com:stograde/cs284-specs.git') == 'MCA'

    _, err = capsys.readouterr()

    assert err == ('Course SD inferred from specs\n'
                   'Course SD inferred from specs\n'
                   'Course HD inferred from specs\n'
                   'Course HD inferred from specs\n'
                   'Course ADS inferred from specs\n'
                   'Course ADS inferred from specs\n'
                   'Course OS inferred from specs\n'
                   'Course OS inferred from specs\n'
                   'Course MCA inferred from specs\n'
                   'Course MCA inferred from specs\n')


def test_get_course_from_spec_url_invalid(capsys):
    assert get_course_from_spec_url('bad_url') == 'SD'

    _, err = capsys.readouterr()

    assert err == ('Could not determine course from url: bad_url\n'
                   'Defaulting to SD\n')


def test_default_course(capsys):
    assert default_course() == 'SD'

    _, err = capsys.readouterr()

    assert err == 'Defaulting to SD\n'
