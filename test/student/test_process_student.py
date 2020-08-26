import os
from unittest import mock

from stograde.common import chdir
from stograde.process_assignment.record_result import RecordResult
from stograde.process_assignment.submission_warnings import SubmissionWarnings
from stograde.specs.spec import Spec
from stograde.student.process_student import prepare_student, process_student
from test.utils import git, touch


@mock.patch('stograde.student.process_student.reset')
@mock.patch('stograde.student.process_student.prepare_student')
def test_process_student_prepare_student_call(mock_prepare, mock_reset):
    process_student(student='student',
                    analyze=False,
                    basedir='',
                    clean=False,
                    date='a_date',
                    interact=False,
                    record=False,
                    skip_branch_check=False,
                    skip_repo_update=False,
                    skip_web_compile=False,
                    specs=[],
                    stogit_url='a_url')

    assert mock_prepare.called
    assert mock_prepare.call_args == (('student', 'a_url'), {'do_clean': False,
                                                             'do_clone': True,
                                                             'do_pull': True,
                                                             'do_checkout': True,
                                                             'date': 'a_date'})

    assert mock_reset.called


@mock.patch('stograde.student.process_student.prepare_student')
def test_process_student_prepare_student_call_skip_repo_update(mock_prepare):
    process_student(student='student',
                    analyze=False,
                    basedir='',
                    clean=False,
                    date='',
                    interact=False,
                    record=False,
                    skip_branch_check=False,
                    skip_repo_update=True,
                    skip_web_compile=False,
                    specs=[],
                    stogit_url='a_url')

    assert mock_prepare.called
    assert mock_prepare.call_args == (('student', 'a_url'), {'do_clean': False,
                                                             'do_clone': False,
                                                             'do_pull': False,
                                                             'do_checkout': True,
                                                             'date': ''})


@mock.patch('stograde.toolkit.global_vars.CI', True)
@mock.patch('stograde.student.process_student.prepare_student')
def test_process_student_prepare_student_call_ci(mock_prepare):
    process_student(student='student',
                    analyze=False,
                    basedir='',
                    clean=False,
                    date='',
                    interact=False,
                    record=False,
                    skip_branch_check=False,
                    skip_repo_update=False,
                    skip_web_compile=False,
                    specs=[],
                    stogit_url='a_url')

    assert mock_prepare.called
    assert mock_prepare.call_args == (('student', 'a_url'), {'do_clean': False,
                                                             'do_clone': False,
                                                             'do_pull': False,
                                                             'do_checkout': False,
                                                             'date': ''})


@mock.patch('stograde.student.process_student.analyze_student')
@mock.patch('stograde.student.process_student.record_student')
def test_process_student_record(mock_record, mock_analyze):
    process_student(student='student',
                    analyze=False,
                    basedir='',
                    clean=False,
                    date='',
                    interact=False,
                    record=True,
                    skip_branch_check=False,
                    skip_repo_update=True,
                    skip_web_compile=False,
                    specs=[],
                    stogit_url='')

    assert mock_record.called
    assert not mock_analyze.called


@mock.patch('stograde.student.process_student.analyze_student')
@mock.patch('stograde.student.process_student.record_student')
def test_process_student_analyze(mock_record, mock_analyze):
    process_student(student='student',
                    analyze=True,
                    basedir='',
                    clean=False,
                    date='',
                    interact=False,
                    record=False,
                    skip_branch_check=False,
                    skip_repo_update=True,
                    skip_web_compile=False,
                    specs=[],
                    stogit_url='')

    assert not mock_record.called
    assert mock_analyze.called


def test_process_student_unmerged_branches(tmpdir):
    with tmpdir.as_cwd():
        os.makedirs('student')
        with chdir('student'):
            git('init')
            git('config', 'user.email', 'an_email@email_provider.com')
            git('config', 'user.name', 'Some Random Name')

            touch('file1')
            git('add', 'file1')
            git('commit', '-m', 'initial')

            git('checkout', '-b', 'branch')

            touch('file2')
            git('add', 'file2')
            git('commit', '-m', 'newcommit')

            git('checkout', 'master')

        result = process_student(student='student',
                                 analyze=True,
                                 basedir='',
                                 clean=False,
                                 date='',
                                 interact=False,
                                 record=True,
                                 skip_branch_check=False,
                                 skip_repo_update=True,
                                 skip_web_compile=False,
                                 specs=[Spec('hw1', 'hw1', architecture=None),
                                        Spec('lab1', 'lab1', architecture=None),
                                        Spec('ws1', 'ws1', architecture=None)],
                                 stogit_url='')

    assert result.results == [RecordResult('hw1', 'student',
                                           warnings=SubmissionWarnings(assignment_missing=True,
                                                                       unmerged_branches=['branch'])),
                              RecordResult('lab1', 'student',
                                           warnings=SubmissionWarnings(assignment_missing=True,
                                                                       unmerged_branches=['branch'])),
                              RecordResult('ws1', 'student',
                                           warnings=SubmissionWarnings(assignment_missing=True,
                                                                       unmerged_branches=['branch']))]


@mock.patch('stograde.student.process_student.prepare_student',
            side_effect=KeyError('An exception was thrown'))
def test_process_student_error(mock_prepare):
    student_result = process_student(student='student',
                                     analyze=False,
                                     basedir='',
                                     clean=False,
                                     date='',
                                     interact=False,
                                     record=False,
                                     skip_branch_check=False,
                                     skip_repo_update=True,
                                     skip_web_compile=False,
                                     specs=[],
                                     stogit_url='')

    assert student_result.name == 'student'
    assert student_result.error == "'An exception was thrown'"
    assert mock_prepare.called


@mock.patch('stograde.toolkit.global_vars.DEBUG', True)
@mock.patch('stograde.student.process_student.prepare_student',
            side_effect=KeyError('An exception was thrown'))
def test_process_student_error_debug(mock_prepare):
    try:
        process_student(student='student',
                        analyze=False,
                        basedir='',
                        clean=False,
                        date='',
                        interact=False,
                        record=False,
                        skip_branch_check=False,
                        skip_repo_update=True,
                        skip_web_compile=False,
                        specs=[],
                        stogit_url='')
        raise AssertionError
    except KeyError:
        pass

    assert mock_prepare.called


# ----------------------------- prepare_student -----------------------------

@mock.patch('stograde.student.process_student.checkout_date')
@mock.patch('stograde.student.process_student.pull')
@mock.patch('stograde.student.process_student.stash')
@mock.patch('stograde.student.process_student.clone_student')
@mock.patch('stograde.student.process_student.remove')
def test_prepare_student_clean(mock_remove, mock_clone, mock_stash, mock_pull, mock_checkout):
    prepare_student(student='',
                    stogit_url='',
                    do_clean=True,
                    do_clone=False,
                    do_pull=False,
                    do_checkout=False)

    assert mock_remove.called
    assert not mock_clone.called
    assert not mock_stash.called
    assert not mock_pull.called
    assert not mock_checkout.called


@mock.patch('stograde.student.process_student.checkout_date')
@mock.patch('stograde.student.process_student.pull')
@mock.patch('stograde.student.process_student.stash')
@mock.patch('stograde.student.process_student.clone_student')
@mock.patch('stograde.student.process_student.remove')
def test_prepare_student_clone(mock_remove, mock_clone, mock_stash, mock_pull, mock_checkout):
    prepare_student(student='',
                    stogit_url='',
                    do_clean=False,
                    do_clone=True,
                    do_pull=False,
                    do_checkout=False)

    assert not mock_remove.called
    assert mock_clone.called
    assert not mock_stash.called
    assert not mock_pull.called
    assert not mock_checkout.called


@mock.patch('stograde.student.process_student.checkout_date')
@mock.patch('stograde.student.process_student.pull')
@mock.patch('stograde.student.process_student.stash')
@mock.patch('stograde.student.process_student.clone_student')
@mock.patch('stograde.student.process_student.remove')
def test_prepare_student_pull(mock_remove, mock_clone, mock_stash, mock_pull, mock_checkout):
    prepare_student(student='',
                    stogit_url='',
                    do_clean=False,
                    do_clone=False,
                    do_pull=True,
                    do_checkout=False)

    assert not mock_remove.called
    assert not mock_clone.called
    assert mock_stash.called
    assert mock_pull.called
    assert not mock_checkout.called


@mock.patch('stograde.student.process_student.checkout_date')
@mock.patch('stograde.student.process_student.pull')
@mock.patch('stograde.student.process_student.stash')
@mock.patch('stograde.student.process_student.clone_student')
@mock.patch('stograde.student.process_student.remove')
def test_prepare_student_checkout(mock_remove, mock_clone, mock_stash, mock_pull, mock_checkout):
    prepare_student(student='',
                    stogit_url='',
                    do_clean=False,
                    do_clone=False,
                    do_pull=False,
                    do_checkout=True)

    assert not mock_remove.called
    assert not mock_clone.called
    assert not mock_stash.called
    assert not mock_pull.called
    assert mock_checkout.called
