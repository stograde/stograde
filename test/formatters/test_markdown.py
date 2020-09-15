import re
import textwrap
from unittest import mock

from stograde.common.run_status import RunStatus
from stograde.formatters.format_type import FormatType
from stograde.formatters.markdown import format_file_contents, get_file_extension, format_file_compilation, \
    format_file_tests, format_file, format_warnings, format_header, format_files_list, format_assignment_markdown
from stograde.process_assignment.record_result import RecordResult
from stograde.process_assignment.submission_warnings import SubmissionWarnings
from stograde.process_file.compile_result import CompileResult
from stograde.process_file.file_result import FileResult
from stograde.process_file.test_result import TestResult

compile_results = [CompileResult('test command', '', RunStatus.SUCCESS),
                   CompileResult('test command 2', 'some output', RunStatus.SUCCESS)]
test_results = [TestResult('test command', '', error=False, status=RunStatus.SUCCESS),
                TestResult('other command', 'some more output\nand another line', error=False,
                           status=RunStatus.SUCCESS),
                TestResult('a third command', 'more output\nand lines\nand more lines\nand yet more lines...',
                           error=False, status=RunStatus.SUCCESS, truncated=True, truncated_after=4)]
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


# ----------------------------- format_assignment_markdown -----------------------------

def test_format_assignment_markdown():
    formatted = format_assignment_markdown(RecordResult(spec_id='lab1',
                                                        student='student4',
                                                        first_submission='4/14/2020 16:04:05',
                                                        warnings=SubmissionWarnings(),
                                                        file_results=file_results))

    assert formatted.assignment == 'lab1'
    assert formatted.student == 'student4'
    assert formatted.type is FormatType.MD
    assert '\n' + formatted.content == textwrap.dedent('''
        # lab1 – student4
        First submission for lab1: 4/14/2020 16:04:05


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


def test_format_assignment_markdown_error():
    # noinspection PyTypeChecker
    formatted = format_assignment_markdown(RecordResult(spec_id='hw1', student='student5',
                                                        file_results=5))

    assert formatted.assignment == 'hw1'
    assert formatted.student == 'student5'
    assert formatted.type is FormatType.MD
    assert re.compile(r"^```\nTraceback \(most recent call last\):"
                      r"[\s\S]*"
                      r"TypeError: 'int' object is not iterable\n\n```$").match(formatted.content)


@mock.patch('stograde.toolkit.global_vars.DEBUG', True)
def test_format_assignment_markdown_error_debug():
    try:
        # noinspection PyTypeChecker
        format_assignment_markdown(RecordResult(spec_id='hw1', student='student5',
                                                file_results=5))
        raise AssertionError
    except TypeError:
        pass


# ----------------------------- format_files_list -----------------------------

def test_format_files_list():
    formatted = format_files_list(file_results)

    assert '\n' + formatted == textwrap.dedent('''


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


# ----------------------------- format_header -----------------------------

def test_format_header_no_warnings():
    formatted = format_header(RecordResult('hw1', 'student1', '4/14/2020 13:22:45'), '')

    assert '\n' + formatted == textwrap.dedent('''
        # hw1 – student1
        First submission for hw1: 4/14/2020 13:22:45
        ''')


def test_format_header_with_warnings():
    formatted = format_header(RecordResult('hw1', 'student2'), 'a warning')

    assert '\n' + formatted == textwrap.dedent('''
        # hw1 – student2
        First submission for hw1: ERROR

        a warning
        ''')


def test_format_header_assignment_missing():
    formatted = format_header(RecordResult('hw1', 'student1', '4/14/2020 13:22:45',
                                           SubmissionWarnings(assignment_missing=True)), '')

    assert '\n' + formatted == textwrap.dedent('''
        # hw1 – student1
        ''')


# ----------------------------- format_warnings -----------------------------

def test_format_warnings_none():
    assert format_warnings(SubmissionWarnings()) == ''


def test_format_warnings_missing():
    assert format_warnings(SubmissionWarnings(assignment_missing=True)) == '**No submission found**\n'


def test_format_warnings_unmerged_branches():
    formatted = format_warnings(SubmissionWarnings(unmerged_branches=['a branch', 'another branch']))

    assert '\n' + formatted == textwrap.dedent('''
        ### *Repository has unmerged branches:*
        - a branch
        - another branch''')


def test_format_warnings_record_error():
    assert format_warnings(SubmissionWarnings(recording_err='an error occurred')) == '**Warning: an error occurred**'


# ----------------------------- format_file -----------------------------

def test_format_file():
    formatted = format_file(file_results[0])

    assert '\n' + formatted == textwrap.dedent('''
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

        ''')


def test_format_file_missing():
    formatted = format_file(file_results[1])

    assert '\n' + formatted == textwrap.dedent('''
        ## another_file.txt

        File not found. `ls .` says that these files exist:
        ```
        a_third_file.txt
        more_files.txt
        ```


        ''')


def test_format_file_optional():
    formatted = format_file(file_results[2])

    assert '\n' + formatted == textwrap.dedent('''
        ## optional.txt (**optional submission**)

        File not found. `ls .` says that these files exist:
        ```
        yet_another_file.txt
        ```


        ''')


# ----------------------------- get_file_extension -----------------------------

def test_get_file_extension():
    assert get_file_extension('file.txt') == 'txt'
    assert get_file_extension('another_file.tar.gz') == 'gz'
    assert get_file_extension('no_extension') == ''


# ----------------------------- format_file_contents -----------------------------

def test_format_file_contents_empty():
    assert format_file_contents('', 'some_file.txt') == '*File empty*'
    assert format_file_contents('   \n\t\n  ', 'another_file.txt') == '*File empty*'


def test_format_file_contents_with_contents():
    simple_contents = textwrap.dedent('''
        int main() {
            return 0;
        }''')

    formatted = '\n' + format_file_contents(simple_contents, 'simple.cpp')

    assert formatted == textwrap.dedent('''
        ```cpp

        int main() {
            return 0;
        }
        ```
        ''')


# ----------------------------- format_file_compilation -----------------------------

def test_format_file_compilation_no_warnings():
    formatted = format_file_compilation([compile_results[0]])
    assert formatted == '**no warnings: `test command`**\n'


def test_format_file_compilation_warnings():
    formatted = format_file_compilation([compile_results[1]])
    assert '\n' + formatted == textwrap.dedent('''
        **warnings: `test command 2`**

        ```
        some output
        ```
        ''')


def test_format_file_compilation_multiple_commands():
    formatted = format_file_compilation(compile_results)
    assert '\n' + formatted == textwrap.dedent('''
        **no warnings: `test command`**

        **warnings: `test command 2`**

        ```
        some output
        ```
        ''')


# ----------------------------- format_file_tests -----------------------------

def test_format_file_tests_no_output():
    formatted = format_file_tests([test_results[0]])
    assert '\n' + formatted == textwrap.dedent('''
        **results of `test command`** (status: SUCCESS)
        ''')


def test_format_file_tests_output():
    formatted = format_file_tests([test_results[1]])
    assert '\n' + formatted == textwrap.dedent('''
        **results of `other command`** (status: SUCCESS)

        ```
        some more output
        and another line
        ```
        ''')


def test_format_file_tests_truncated_output():
    formatted = format_file_tests([test_results[2]])
    assert '\n' + formatted == textwrap.dedent('''
        **results of `a third command`** (status: SUCCESS)

        ```
        more output
        and lines
        and more lines
        and yet more lines...
        ```
        *(truncated after 4 lines)*
        ''')


def test_format_file_tests_multiple_commands():
    formatted = format_file_tests(test_results)
    assert '\n' + formatted == textwrap.dedent('''
        **results of `test command`** (status: SUCCESS)

        **results of `other command`** (status: SUCCESS)

        ```
        some more output
        and another line
        ```

        **results of `a third command`** (status: SUCCESS)

        ```
        more output
        and lines
        and more lines
        and yet more lines...
        ```
        *(truncated after 4 lines)*
        ''')
