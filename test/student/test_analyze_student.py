import logging
import os
from unittest import mock

import pytest

from stograde.common import chdir
from stograde.process_assignment.assignment_status import AssignmentStatus
from stograde.specs.spec import Spec
from stograde.specs.spec_file import SpecFile
from stograde.student.analyze_student import analyze_assignment, analyze_student
from stograde.student.student_result import StudentResult
from test.utils import git

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'analyze_test'))
def test_analyze_student(datafiles, caplog):
    student_result = StudentResult('student1')
    with chdir(str(datafiles)):
        git('init')
        git('symbolic-ref', 'HEAD', 'refs/heads/main')  # Workaround for older versions of git without default main
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        git('add', os.path.join('hw1', 'a_file.txt'))
        git('commit', '-m', '"Add file"')

        with caplog.at_level(logging.DEBUG):
            analyze_student(student_result,
                            [Spec('hw1', 'hw1', architecture=None,
                                  files=[SpecFile('a_file.txt')]),
                             Spec('lab1', 'lab1', architecture=None,
                                  files=[SpecFile('b_file.txt')]),
                             Spec('ws1', 'ws1', architecture=None,
                                  files=[SpecFile('c_file.txt')])],
                            check_for_branches=True)

    assert student_result.homeworks == {'hw1': AssignmentStatus.SUCCESS}
    assert student_result.labs == {'lab1': AssignmentStatus.SUCCESS}
    assert student_result.worksheets == {'ws1': AssignmentStatus.SUCCESS}
    assert isinstance(student_result.unmerged_branches, list)
    assert not student_result.unmerged_branches

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {("Analyzing student1's assignments", 'DEBUG')}


@mock.patch('stograde.toolkit.global_vars.CI', True)
@mock.patch('stograde.student.analyze_student.find_unmerged_branches')
@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'analyze_test', 'student1'))
def test_analyze_student_ci(mock_function, datafiles):
    student_result = StudentResult('student1')
    with chdir(str(datafiles)):
        analyze_student(student_result,
                        [Spec('hw1', 'hw1', architecture=None,
                              files=[SpecFile('a_file.txt')]),
                         Spec('lab1', 'lab1', architecture=None,
                              files=[SpecFile('b_file.txt')]),
                         Spec('ws1', 'ws1', architecture=None,
                              files=[SpecFile('c_file.txt')])],
                        check_for_branches=True)

    assert not mock_function.called

    assert student_result.homeworks == {'hw1': AssignmentStatus.SUCCESS}
    assert student_result.labs == {'lab1': AssignmentStatus.SUCCESS}
    assert student_result.worksheets == {'ws1': AssignmentStatus.SUCCESS}


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'analyze_test'))
def test_analyze_assignment_missing_directory(datafiles, caplog):
    spec = Spec('hw1', 'not_a_directory', architecture=None)
    with caplog.at_level(logging.DEBUG):
        with chdir(str(datafiles)):
            assert analyze_assignment(spec) is AssignmentStatus.MISSING

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('Cannot analyze assignment in directory not_a_directory: Does not exist', 'DEBUG')}


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'analyze_test'))
def test_analyze_assignment_success(datafiles):
    spec = Spec('hw1', 'hw1', architecture=None, files=[SpecFile('a_file.txt'),
                                                        SpecFile('b_file.txt')])

    with chdir(str(datafiles)):
        assert analyze_assignment(spec) is AssignmentStatus.SUCCESS


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'analyze_test'))
def test_analyze_assignment_partial(datafiles):
    spec = Spec('hw1', 'hw1', architecture=None, files=[SpecFile('a_file.txt'),
                                                        SpecFile('b_file.txt'),
                                                        SpecFile('c_file.txt')])

    with chdir(str(datafiles)):
        assert analyze_assignment(spec) is AssignmentStatus.PARTIAL


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'analyze_test'))
def test_analyze_assignment_missing_all_files(datafiles):
    spec = Spec('hw1', 'hw1', architecture=None, files=[SpecFile('c_file.txt'),
                                                        SpecFile('d_file.txt')])

    with chdir(str(datafiles)):
        assert analyze_assignment(spec) is AssignmentStatus.MISSING
