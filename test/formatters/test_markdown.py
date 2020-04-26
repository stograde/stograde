import textwrap

from stograde.common.run_status import RunStatus
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

    assert formatted['assignment'] == 'lab1'
    assert formatted['student'] == 'student4'
    assert formatted['type'] == 'md'
    assert '\n' + formatted['content'] == textwrap.dedent('''
        # lab1 – student4
        First submission for lab1: 4/14/2020 16:04:05\n\n
        ## test_file.txt (a modification time)\n
        ```txt
        some file contents
        and another line
        ```\n\n
        **no warnings: `a command`**\n
        **warnings: `another command`**\n
        ```
        output text
        ```\n\n
        **results of `a test command`** (status: SUCCESS)\n
        **results of `other test command`** (status: FILE_NOT_FOUND)\n
        ```
        more output
        another line
        ```\n\n\n
        ## another_file.txt\n
        File not found. `ls .` says that these files exist:
        ```
        a_third_file.txt
        more_files.txt
        ```\n\n\n\n
        ## optional.txt (**optional submission**)\n
        File not found. `ls .` says that these files exist:
        ```
        yet_another_file.txt
        ```\n\n\n\n
        ''')


# ----------------------------- format_files_list -----------------------------

def test_format_files_list():
    formatted = format_files_list(file_results)

    assert '\n' + formatted == textwrap.dedent('''\n\n
        ## test_file.txt (a modification time)\n
        ```txt
        some file contents
        and another line
        ```\n\n
        **no warnings: `a command`**\n
        **warnings: `another command`**\n
        ```
        output text
        ```\n\n
        **results of `a test command`** (status: SUCCESS)\n
        **results of `other test command`** (status: FILE_NOT_FOUND)\n
        ```
        more output
        another line
        ```\n\n\n
        ## another_file.txt\n
        File not found. `ls .` says that these files exist:
        ```
        a_third_file.txt
        more_files.txt
        ```\n\n\n\n
        ## optional.txt (**optional submission**)\n
        File not found. `ls .` says that these files exist:
        ```
        yet_another_file.txt
        ```\n\n
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
        First submission for hw1: ERROR\n
        a warning
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
        ## test_file.txt (a modification time)\n
        ```txt
        some file contents
        and another line
        ```\n\n
        **no warnings: `a command`**\n
        **warnings: `another command`**\n
        ```
        output text
        ```\n\n
        **results of `a test command`** (status: SUCCESS)\n
        **results of `other test command`** (status: FILE_NOT_FOUND)\n
        ```
        more output
        another line
        ```\n
        ''')


def test_format_file_missing():
    formatted = format_file(file_results[1])

    assert '\n' + formatted == textwrap.dedent('''
        ## another_file.txt\n
        File not found. `ls .` says that these files exist:
        ```
        a_third_file.txt
        more_files.txt
        ```\n\n
        ''')


def test_format_file_optional():
    formatted = format_file(file_results[2])

    assert '\n' + formatted == textwrap.dedent('''
        ## optional.txt (**optional submission**)\n
        File not found. `ls .` says that these files exist:
        ```
        yet_another_file.txt
        ```\n\n
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
        ```cpp\n
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
        **warnings: `test command 2`**\n
        ```
        some output
        ```
        ''')


def test_format_file_compilation_multiple_commands():
    formatted = format_file_compilation(compile_results)
    assert '\n' + formatted == textwrap.dedent('''
        **no warnings: `test command`**\n
        **warnings: `test command 2`**\n
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
        **results of `other command`** (status: SUCCESS)\n
        ```
        some more output
        and another line
        ```
        ''')


def test_format_file_tests_truncated_output():
    formatted = format_file_tests([test_results[2]])
    assert '\n' + formatted == textwrap.dedent('''
        **results of `a third command`** (status: SUCCESS)\n
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
        **results of `test command`** (status: SUCCESS)\n
        **results of `other command`** (status: SUCCESS)\n
        ```
        some more output
        and another line
        ```\n
        **results of `a third command`** (status: SUCCESS)\n
        ```
        more output
        and lines
        and more lines
        and yet more lines...
        ```
        *(truncated after 4 lines)*
        ''')
