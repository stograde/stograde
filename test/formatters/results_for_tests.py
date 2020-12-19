from stograde.common.run_status import RunStatus
from stograde.process_file.compile_result import CompileResult
from stograde.process_file.file_result import FileResult
from stograde.process_file.test_result import TestResult

compile_results = [CompileResult('test command', '', status=RunStatus.SUCCESS),
                   CompileResult('test command 2', 'some output', status=RunStatus.SUCCESS),
                   CompileResult('test command 3', 'more', status=RunStatus.SUCCESS, truncated_after=4)]
test_results = [TestResult('test command', '', error=False, status=RunStatus.SUCCESS),
                TestResult('other command', 'some more output\nand another line', error=False,
                           status=RunStatus.SUCCESS),
                TestResult('a third command', 'more',
                           error=False, status=RunStatus.SUCCESS, truncated_after=4)]
file_results = [FileResult(file_name='test_file.txt',
                           contents='some file contents\nand another line',
                           compile_results=[CompileResult('a command', '', RunStatus.SUCCESS),
                                            CompileResult('another command', 'output text', RunStatus.SUCCESS)],
                           test_results=[TestResult('a test command', '', error=False, status=RunStatus.SUCCESS),
                                         TestResult('other test command', 'more output\nanother line',
                                                    error=True, status=RunStatus.FILE_NOT_FOUND)],
                           last_modified='a modification time'),
                FileResult(file_name='another_file.txt',
                           file_missing=True,
                           other_files=['a_third_file.txt', 'more_files.txt']),
                FileResult(file_name='optional.txt',
                           file_missing=True,
                           other_files=['yet_another_file.txt'],
                           optional=True),
                FileResult(file_name='truncated.txt',
                           contents='some tex',
                           truncated_after=8,
                           last_modified='a modification time')]
