import os
import textwrap
from unittest import mock

from stograde.common.run_status import RunStatus
from stograde.formatters.format_type import FormatType
from stograde.formatters.formatted_result import FormattedResult
from stograde.process_assignment.record_result import RecordResult
from stograde.process_assignment.submission_warnings import SubmissionWarnings
from stograde.process_file.compile_result import CompileResult
from stograde.process_file.file_result import FileResult
from stograde.process_file.test_result import TestResult
from stograde.student.student_result import StudentResult
from stograde.toolkit.save_recordings import record_recording_to_disk, save_recordings


def test_record_recording_to_disk(tmpdir):
    with tmpdir.as_cwd():
        record_recording_to_disk([FormattedResult(assignment='hw1',
                                                  content='some content',
                                                  student='z',
                                                  type=FormatType.MD),
                                  FormattedResult(assignment='hw1',
                                                  content='some more content',
                                                  student='a',
                                                  type=FormatType.MD),
                                  FormattedResult(assignment='hw1',
                                                  content='even more content',
                                                  student='b',
                                                  type=FormatType.MD)],
                                 file_identifier='hw1',
                                 format_type=FormatType.MD)

        assert os.path.exists(os.path.join('logs', 'log-hw1.md'))

        with open(os.path.join('logs', 'log-hw1.md')) as file:
            contents = file.read()
            file.close()

        assert contents == ('some more content\n'
                            'even more content\n'
                            'some content')


def test_record_recording_to_disk_error(capsys):
    with mock.patch('os.makedirs', side_effect=TypeError('An error was thrown')):
        record_recording_to_disk([], 'hw1', FormatType.MD)

    _, err = capsys.readouterr()

    assert err == 'Could not write recording for hw1: An error was thrown\n'


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
                           optional=True)]


def test_save_recordings_disk(tmpdir):
    with tmpdir.as_cwd():
        save_recordings([StudentResult(name='z',
                                       results=[RecordResult(spec_id='hw1',
                                                             student='student4',
                                                             first_submission='4/14/2020 16:04:05',
                                                             warnings=SubmissionWarnings(),
                                                             file_results=file_results)])],
                        '',
                        False)

        assert os.path.exists(os.path.join('logs', 'log-hw1.md'))

        with open(os.path.join('logs', 'log-hw1.md')) as file:
            contents = file.read()
            file.close()

        assert '\n' + contents == textwrap.dedent('''
                # hw1 – student4
                First submission for hw1: 4/14/2020 16:04:05


                ## test_file.txt (a modification time)

                ```txt
                some file contents
                and another line
                ```


                **no warnings: `a command`**

                **warnings: `another command`**

                ```
                output text
                ```


                **results of `a test command`** (status: SUCCESS)

                **results of `other test command`** (status: FILE_NOT_FOUND)

                ```
                more output
                another line
                ```



                ## another_file.txt

                File not found. `ls .` says that these files exist:
                ```
                a_third_file.txt
                more_files.txt
                ```




                ## optional.txt (**optional submission**)

                File not found. `ls .` says that these files exist:
                ```
                yet_another_file.txt
                ```




                ''')


def test_save_recording_gist(capsys):
    with mock.patch('stograde.toolkit.save_recordings.post_gist') as mock_gist:
        mock_gist.return_value = 'a_url'
        save_recordings([StudentResult(name='z',
                                       results=[RecordResult(spec_id='hw1',
                                                             student='student4',
                                                             first_submission='4/14/2020 16:04:05',
                                                             warnings=SubmissionWarnings(),
                                                             file_results=file_results)])],
                        'the table',
                        True)

        assert mock_gist.call_args[0][0] == 'log for hw1'
        assert mock_gist.call_args[0][1] == {'-stograde report hw1 table.txt': {'content': 'the table'},
                                             'student4.md':
                                                 {'content': '# hw1 – student4\n'
                                                             'First submission for hw1: 4/14/2020 16:04:05\n\n\n'
                                                             '## test_file.txt (a modification time)\n\n'
                                                             '```txt\n'
                                                             'some file contents\n'
                                                             'and another line\n'
                                                             '```\n\n\n'
                                                             '**no warnings: `a command`**\n\n'
                                                             '**warnings: `another command`**\n\n'
                                                             '```\n'
                                                             'output text\n'
                                                             '```\n\n\n'
                                                             '**results of `a test command`** (status: SUCCESS)\n\n'
                                                             '**results of `other test command`** '
                                                             '(status: FILE_NOT_FOUND)\n\n'
                                                             '```\n'
                                                             'more output\n'
                                                             'another line\n'
                                                             '```\n\n\n\n'
                                                             '## another_file.txt\n\n'
                                                             'File not found. `ls .` says that these files exist:\n'
                                                             '```\n'
                                                             'a_third_file.txt\n'
                                                             'more_files.txt\n'
                                                             '```\n\n\n\n\n'
                                                             '## optional.txt (**optional submission**)\n\n'
                                                             'File not found. `ls .` says that these files exist:\n'
                                                             '```\n'
                                                             'yet_another_file.txt\n'
                                                             '```'}}

    out, _ = capsys.readouterr()

    assert out == 'hw1 results are available at a_url\n'


def test_save_recording_bad_formatter():
    try:
        # noinspection PyTypeChecker
        save_recordings([], '', False, 5)
        raise AssertionError
    except ValueError:
        pass
