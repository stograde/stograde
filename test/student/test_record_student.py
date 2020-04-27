import logging
import os

import pytest

from stograde.common import chdir
from stograde.process_assignment.record_result import RecordResult
from stograde.process_assignment.submission_warnings import SubmissionWarnings
from stograde.process_file.file_result import FileResult
from stograde.specs.file_options import FileOptions
from stograde.specs.spec import Spec
from stograde.specs.spec_file import SpecFile
from stograde.student import record_student
from stograde.student.student_result import StudentResult
from test.utils import git

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_record_student(datafiles):
    student_result = StudentResult('student1')
    specs = [Spec('hw1', 'hw1', architecture=None,
                  files=[SpecFile('a_file.txt', [], [], FileOptions())]),
             Spec('hw2', 'hw2', architecture=None,
                  files=[SpecFile('b_file.txt', [], [], FileOptions())])]

    with chdir(str(datafiles)):
        with chdir('student1'):
            git('init')
            git('config', 'user.email', 'an_email@email_provider.com')
            git('config', 'user.name', 'Some Random Name')

            git('add', os.path.join('hw1', 'a_file.txt'))
            git('commit', '-m', '"Add file"', '--date="Tue Apr 21 12:28:03 2020 -0500"')

            git('add', os.path.join('hw2', 'b_file.txt'))
            git('commit', '-m', '"Add another file"', '--date="Sat Apr 25 20:27:05 2020 -0500"')

        record_student(student=student_result,
                       specs=specs,
                       basedir='',
                       interact=False,
                       skip_web_compile=False)

    assert student_result.results[0].student == 'student1'
    assert student_result.results[0].spec_id == 'hw1'
    assert student_result.results[0].first_submission == 'Tue Apr 21 12:28:03 2020 -0500'
    assert student_result.results[0].file_results == [FileResult(file_name='a_file.txt',
                                                                 last_modified='Tue Apr 21 12:28:03 2020 -0500')]

    assert student_result.results[1].student == 'student1'
    assert student_result.results[1].spec_id == 'hw2'
    assert student_result.results[1].first_submission == 'Sat Apr 25 20:27:05 2020 -0500'
    assert student_result.results[1].file_results == [FileResult(file_name='b_file.txt',
                                                                 last_modified='Sat Apr 25 20:27:05 2020 -0500')]


def test_record_student_no_specs():
    student = StudentResult('name')
    record_student(student=student, specs=[], basedir='.',
                   interact=False, skip_web_compile=False)

    assert student.results == []


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_record_student_assignment_folder_missing(datafiles, caplog):
    student = StudentResult('student1')
    # student1 has a hw1 directory but not an another_folder directory
    with chdir(str(datafiles)):
        with caplog.at_level(logging.DEBUG):
            record_student(student=student,
                           specs=[Spec('hw1', 'another_folder', None)],
                           basedir='.',
                           interact=False,
                           skip_web_compile=False)

    assert student.results == [RecordResult('hw1', 'student1',
                                            warnings=SubmissionWarnings(assignment_missing=True))]

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {("Recording student1's hw1", 'DEBUG')}
