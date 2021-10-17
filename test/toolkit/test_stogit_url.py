import datetime
import os

from stograde.common import chdir
from stograde.toolkit.stogit_url import compute_stogit_url, get_course_from_specs
from test.utils import git


def test_compute_stogit_url_infer_course(tmpdir, capsys):
    with tmpdir.as_cwd():
        os.makedirs('data')
        with chdir('data'):
            git('init')
            git('remote', 'add', 'origin', 'https://github.com/stograde/cs251-specs.git')
        assert compute_stogit_url(stogit='',
                                  course='',
                                  _now=datetime.date(2020, 4, 16)) == 'git@stogit.cs.stolaf.edu:sd/s20'

    _, err = capsys.readouterr()

    assert err == 'Course SD inferred from specs\n'


def test_compute_stogit_url_course_date_spring():
    assert compute_stogit_url(stogit='',
                              course='sd',
                              _now=datetime.date(2017, 1, 31)) == 'git@stogit.cs.stolaf.edu:sd/s17'


def test_compute_stogit_url_course_date_fall():
    assert compute_stogit_url(stogit='',
                              course='hd',
                              _now=datetime.date(2016, 9, 15)) == 'git@stogit.cs.stolaf.edu:hd/f16'


def test_compute_stogit_url_stogit_set():
    assert compute_stogit_url(stogit='blah',
                              course='sd') == 'blah'


def test_compute_stogit_url_course_with_semester():
    assert compute_stogit_url(stogit='',
                              course='hd/f19') == 'git@stogit.cs.stolaf.edu:hd/f19'


def test_get_course_from_specs_sd(tmpdir):
    with tmpdir.as_cwd():
        os.makedirs('data')
        with chdir('data'):
            git('init')
            git('remote', 'add', 'origin', 'https://github.com/stograde/cs251-specs.git')
        assert get_course_from_specs() == 'SD'


def test_get_course_from_specs_hd(tmpdir):
    with tmpdir.as_cwd():
        os.makedirs('data')
        with chdir('data'):
            git('init')
            git('remote', 'add', 'origin', 'https://github.com/stograde/cs241-specs.git')
        assert get_course_from_specs() == 'HD'


def test_get_course_from_specs_ads(tmpdir):
    with tmpdir.as_cwd():
        os.makedirs('data')
        with chdir('data'):
            git('init')
            git('remote', 'add', 'origin', 'https://github.com/stograde/cs253-specs.git')
        assert get_course_from_specs() == 'ADS'


def test_get_course_from_specs_os(tmpdir):
    with tmpdir.as_cwd():
        os.makedirs('data')
        with chdir('data'):
            git('init')
            git('remote', 'add', 'origin', 'https://github.com/stograde/cs273-specs.git')
        assert get_course_from_specs() == 'OS'


def test_get_course_from_specs_fallback(tmpdir, capsys):
    with tmpdir.as_cwd():
        os.makedirs('data')
        with chdir('data'):
            git('init')
            git('remote', 'add', 'origin', 'https://github.com/stograde/stograde.git')
        assert get_course_from_specs() == 'SD'

    _, err = capsys.readouterr()

    assert err == ('Could not determine course from url: https://github.com/stograde/stograde.git\n'
                   'Defaulting to SD\n')


def test_get_course_from_specs_fallback_git_failure(tmpdir, capsys):
    with tmpdir.as_cwd():
        os.makedirs('data')
        with chdir('data'):
            git('init')
        assert get_course_from_specs() == 'SD'

    _, err = capsys.readouterr()

    assert err == ('Could not get URL from data directory: '
                   "Command '['git', 'config', '--get', 'remote.origin.url']' returned non-zero exit status 1.\n"
                   'Defaulting to SD\n')


def test_get_course_from_specs_failure_no_data_dir(capsys):
    try:
        get_course_from_specs()
    except SystemExit:
        pass

    _, err = capsys.readouterr()

    assert err == 'Unable to determine course from specs: no data directory\n'
