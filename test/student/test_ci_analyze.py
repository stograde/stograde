from stograde.common.run_status import RunStatus
from stograde.process_assignment.record_result import RecordResult
from stograde.process_file.compile_result import CompileResult
from stograde.process_file.file_result import FileResult
from stograde.student import ci_analyze
from stograde.student.student_result import StudentResult


def test_ci_analyze_passing():
    passing = ci_analyze(StudentResult(name='student2',
                                       results=[RecordResult(spec_id='hw1',
                                                             student='student2',
                                                             file_results=[FileResult('test_file1.txt')])]))

    assert passing is True


def test_ci_analyze_failing_with_missing_file(caplog):
    passing = ci_analyze(StudentResult(name='student2',
                                       results=[RecordResult(spec_id='hw2',
                                                             student='student2',
                                                             file_results=[FileResult(file_name='missing.txt',
                                                                                      file_missing=True)])]))

    assert passing is False

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('hw2: File missing.txt missing', 'ERROR')}


def test_ci_analyze_passing_with_missing_file_because_lab(caplog):
    passing = ci_analyze(StudentResult(name='student2',
                                       results=[RecordResult(spec_id='lab3',
                                                             student='student2',
                                                             file_results=[FileResult(file_name='missing.txt',
                                                                                      file_missing=True)])]))

    assert passing is True

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('lab3: File missing.txt missing', 'ERROR')}


def test_ci_analyze_failing_with_failed_compile(caplog):
    file_result = FileResult(file_name='test_file2.txt',
                             compile_results=[CompileResult(command='a command',
                                                            output='the file was not found\nanother line',
                                                            status=RunStatus.CALLED_PROCESS_ERROR)])

    passing = ci_analyze(StudentResult(name='student2',
                                       results=[RecordResult(spec_id='hw4',
                                                             student='student2',
                                                             file_results=[file_result])]))

    assert passing is False

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('hw4: File test_file2.txt compile error:\n\n'
                             '\tthe file was not found\n'
                             '\tanother line', 'ERROR')}


def test_ci_analyze_passing_with_failed_compile_because_optional(caplog):
    file_result = FileResult(file_name='test_file3.txt',
                             compile_results=[CompileResult(command='a command',
                                                            output='the file was not found\nanother line',
                                                            status=RunStatus.CALLED_PROCESS_ERROR)],
                             optional=True)

    passing = ci_analyze(StudentResult(name='student2',
                                       results=[RecordResult(spec_id='hw5',
                                                             student='student2',
                                                             file_results=[file_result])]))

    assert passing is True

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('hw5: File test_file3.txt compile error (This did not fail the build)', 'WARNING')}


def test_ci_analyze_passing_with_failed_compile_because_lab(caplog):
    file_result = FileResult(file_name='test_file4.txt',
                             compile_results=[CompileResult(command='a command',
                                                            output='the file was not found\nanother line',
                                                            status=RunStatus.CALLED_PROCESS_ERROR)])

    passing = ci_analyze(StudentResult(name='student2',
                                       results=[RecordResult(spec_id='lab6',
                                                             student='student2',
                                                             file_results=[file_result])]))

    assert passing is True

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('lab6: File test_file4.txt compile error:\n\n'
                             '\tthe file was not found\n'
                             '\tanother line', 'ERROR')}
