import os
from unittest import mock

import pytest

from stograde.common import chdir
from stograde.process_assignment.process_assignment import process_assignment, remove_execs
from stograde.process_assignment.submission_warnings import SubmissionWarnings
from stograde.process_file.file_result import FileResult
from stograde.specs.file_options import FileOptions
from stograde.specs.spec import Spec
from stograde.specs.spec_file import SpecFile
from stograde.student.student_result import StudentResult
from test.utils import git, touch

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'process_assignment'))
def test_process_assignment(datafiles):
    student_result = StudentResult('student1')
    spec = Spec('hw1', 'hw1', architecture=None,
                files=[SpecFile('a_file.txt', [], [], [], FileOptions()),
                       SpecFile('b_file.txt', [], [], [], FileOptions())])

    with chdir(str(datafiles)):
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        git('add', 'a_file.txt')
        git('commit', '-m', '"Add file"', '--date="Tue Apr 21 12:28:03 2020 -0500"')

        git('add', 'b_file.txt')
        git('commit', '-m', '"Add another file"', '--date="Sat Apr 25 20:27:05 2020 -0500"')

        result = process_assignment(student=student_result,
                                    spec=spec,
                                    basedir='',
                                    interact=False,
                                    skip_web_compile=False)

    assert result.student == 'student1'
    assert result.spec_id == 'hw1'
    assert result.first_submission == 'Tue Apr 21 12:28:03 2020 -0500'
    assert result.file_results == [FileResult(file_name='a_file.txt',
                                              last_modified='Tue Apr 21 12:28:03 2020 -0500'),
                                   FileResult(file_name='b_file.txt',
                                              last_modified='Sat Apr 25 20:27:05 2020 -0500')]


@mock.patch('stograde.process_assignment.process_assignment.remove_execs',
            side_effect=KeyError('An exception was thrown'))
def test_process_assignment_with_error(mock_function):
    student_result = StudentResult('student1')
    spec = Spec('hw1', 'hw1', architecture=None)
    result = process_assignment(student=student_result,
                                spec=spec,
                                basedir='',
                                interact=False,
                                skip_web_compile=False)

    assert mock_function.called
    assert result.student == 'student1'
    assert result.spec_id == 'hw1'
    assert result.warnings == SubmissionWarnings(recording_err="'An exception was thrown'")


@mock.patch('stograde.toolkit.global_vars.DEBUG', True)
@mock.patch('stograde.process_assignment.process_assignment.remove_execs',
            side_effect=KeyError('An exception was thrown'))
def test_process_assignment_with_error_debug(mock_function):
    student_result = StudentResult('student1')
    spec = Spec('hw1', 'hw1', architecture=None)
    try:
        process_assignment(student=student_result,
                           spec=spec,
                           basedir='',
                           interact=False,
                           skip_web_compile=False)
        raise AssertionError
    except KeyError:
        pass

    assert mock_function.called


@mock.patch('stograde.toolkit.global_vars.CI', True)
@mock.patch('stograde.process_assignment.process_assignment.get_assignment_first_submit_time')
def test_process_assignment_ci(mock_function):
    student_result = StudentResult('student1')
    spec = Spec('hw1', 'hw1', architecture=None)
    process_assignment(student=student_result,
                       spec=spec,
                       basedir='',
                       interact=False,
                       skip_web_compile=False)

    assert not mock_function.called


def test_remove_execs(tmpdir):
    spec = Spec('hw2', 'hw2', architecture=None,
                files=[SpecFile('a_file.txt', [], [], [], FileOptions()),
                       SpecFile('file', [], [], [], FileOptions()),
                       SpecFile('test.cpp', ['Test.cpp', 'TEST.cpp'], [], [], FileOptions())])

    with tmpdir.as_cwd():
        touch('non_exec_file.txt')
        touch('file.exec')
        touch('non_spec_exec.exec')
        touch('test.cpp.exec')
        touch('Test.cpp.exec')

        assert set(os.listdir('.')) == {'non_exec_file.txt', 'file.exec', 'non_spec_exec.exec',
                                        'test.cpp.exec', 'Test.cpp.exec'}

        remove_execs(spec)

        assert set(os.listdir('.')) == {'non_exec_file.txt', 'non_spec_exec.exec'}
