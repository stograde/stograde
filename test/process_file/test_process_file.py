import os
import textwrap

import pytest

from stograde.common import chdir
from stograde.common.run_status import RunStatus
from stograde.process_file.compile_result import CompileResult
from stograde.process_file.file_result import FileResult
from stograde.process_file.process_file import get_file, parse_command, compile_file, test_file, process_file
from stograde.process_file.test_result import TestResult
from stograde.specs.file_options import FileOptions
from stograde.specs.spec_file import SpecFile
from test.utils import git, touch

_dir = os.path.dirname(os.path.realpath(__file__))


# ----------------------------- get_file -----------------------------

@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_get_file_success(datafiles):
    spec = SpecFile('a_file.txt', [], [], FileOptions())
    result = FileResult(file_name='a_file.txt')

    with chdir(str(datafiles)):
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        git('add', 'a_file.txt')
        git('commit', '-m', '"Add file"', '--date="Tue Apr 21 12:28:03 2020 -0500"')

        ret = get_file(spec, result)

    assert ret is True
    assert result.file_name == 'a_file.txt'
    assert result.contents == 'contents\n'
    assert not result.compile_results
    assert not result.test_results
    assert result.file_missing is False
    assert result.last_modified == 'Tue Apr 21 12:28:03 2020 -0500'
    assert not result.other_files
    assert result.optional is False
    assert result.compile_optional is False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_get_file_hide_contents(datafiles):
    spec = SpecFile('a_file.txt', [], [], FileOptions(hide_contents=True,
                                                      optional=True,
                                                      compile_optional=True))
    result = FileResult(file_name='a_file.txt')

    with chdir(str(datafiles)):
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        git('add', 'a_file.txt')
        git('commit', '-m', '"Add file"', '--date="Tue Apr 21 12:28:03 2020 -0500"')

        ret = get_file(spec, result)

    assert ret is True
    assert result.file_name == 'a_file.txt'
    assert result.contents == ''
    assert not result.compile_results
    assert not result.test_results
    assert result.file_missing is False
    assert result.last_modified == 'Tue Apr 21 12:28:03 2020 -0500'
    assert not result.other_files
    assert result.optional is False
    assert result.compile_optional is True


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_get_file_truncated_contents(datafiles):
    spec = SpecFile('a_file.txt', [], [], FileOptions(truncate_contents=4))
    result = FileResult(file_name='a_file.txt')

    with chdir(str(datafiles)):
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        git('add', 'a_file.txt')
        git('commit', '-m', '"Add file"', '--date="Tue Apr 21 12:28:03 2020 -0500"')

        ret = get_file(spec, result)

    assert ret is True
    assert result.file_name == 'a_file.txt'
    assert result.contents == 'cont'
    assert not result.compile_results
    assert not result.test_results
    assert result.file_missing is False
    assert result.last_modified == 'Tue Apr 21 12:28:03 2020 -0500'
    assert not result.other_files
    assert result.optional is False
    assert result.compile_optional is False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures'))
def test_get_file_missing(datafiles):
    spec = SpecFile('b_file.txt', [], [], FileOptions(optional=True))
    result = FileResult(file_name='b_file.txt')

    with chdir(str(datafiles)):
        ret = get_file(spec, result)

    assert ret is False
    assert result.file_name == 'b_file.txt'
    assert not result.contents
    assert not result.compile_results
    assert not result.test_results
    assert result.file_missing is True
    assert not result.last_modified
    assert set(result.other_files) == {'a_file.txt', 'compile_file', 'process_file', 'test_file'}
    assert result.optional is True
    assert result.compile_optional is False


# ----------------------------- parse_command -----------------------------

def test_parse_command_with_file():
    assert parse_command('g++ --std=c++11 $@ -o $@.exec',
                         file_name='a_file.cpp',
                         supporting_dir='') == 'g++ --std=c++11 ./a_file.cpp -o ./a_file.cpp.exec'


def test_parse_command_with_supporting():
    assert parse_command('cat $SUPPORT',
                         file_name='',
                         supporting_dir='data/supporting/hw1') == 'cat data/supporting/hw1'


def test_parse_command_no_replacements():
    assert parse_command('echo A',
                         file_name='file',
                         supporting_dir='dir') == 'echo A'


# ----------------------------- compile_file -----------------------------

@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'compile_file'))
def test_compile_file_success(datafiles):
    spec = SpecFile(file_name='good.cpp',
                    compile_commands=['g++ --std=c++11 $@ -o $@.exec', 'echo A'],
                    test_commands=[],
                    options=FileOptions())
    result = FileResult(file_name='good.cpp')

    with chdir(str(datafiles)):
        ret = compile_file(file_spec=spec, results=result, supporting_dir='')

    assert ret is True
    assert result.compile_results == [CompileResult(command='g++ --std=c++11 ./good.cpp -o ./good.cpp.exec',
                                                    output='',
                                                    status=RunStatus.SUCCESS),
                                      CompileResult(command='echo A',
                                                    output='A\n',
                                                    status=RunStatus.SUCCESS)]


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'compile_file'))
def test_compile_file_failure(datafiles):
    spec = SpecFile(file_name='bad.cpp',
                    compile_commands=['g++ --std=c++11 $@ -o $@.exec', 'echo A'],
                    test_commands=[],
                    options=FileOptions())
    result = FileResult(file_name='bad.cpp')

    with chdir(str(datafiles)):
        ret = compile_file(file_spec=spec, results=result, supporting_dir='')

    assert ret is False

    for c_result in result.compile_results:
        c_result.output = c_result.output.replace('\r\n', '\n')

    assert result.compile_results == [CompileResult(command='g++ --std=c++11 ./bad.cpp -o ./bad.cpp.exec',
                                                    output='./bad.cpp: In function ‘int main()’:\n'
                                                           './bad.cpp:7:13: error: expected ‘}’ at end of input\n'
                                                           '     return 0;\n'
                                                           '             ^\n',
                                                    status=RunStatus.CALLED_PROCESS_ERROR)]


# ----------------------------- test_file -----------------------------

@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'test_file'))
def test_test_file_success(datafiles):
    spec = SpecFile(file_name='good.cpp',
                    compile_commands=[],
                    test_commands=['make good.cpp.exec', '$@.exec'],
                    options=FileOptions())
    result = FileResult(file_name='good.cpp')

    with chdir(str(datafiles)):
        test_file(file_spec=spec, file_results=result, supporting_dir='', interact=False)

    assert result.test_results == [TestResult(command='make good.cpp.exec',
                                              output='g++ --std=c++11 good.cpp -o good.cpp.exec\n',
                                              error=False,
                                              status=RunStatus.SUCCESS,
                                              truncated=False,
                                              truncated_after=10000),
                                   TestResult(command='./good.cpp.exec',
                                              output='Hello\n',
                                              error=False,
                                              status=RunStatus.SUCCESS,
                                              truncated=False,
                                              truncated_after=10000)]


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'test_file'))
def test_test_file_error(datafiles):
    spec = SpecFile(file_name='error.cpp',
                    compile_commands=[],
                    test_commands=['', 'make error.cpp.exec', '$@.exec'],
                    options=FileOptions())
    result = FileResult(file_name='error.cpp')

    with chdir(str(datafiles)):
        test_file(file_spec=spec, file_results=result, supporting_dir='', interact=False)

    assert result.test_results == [TestResult(command='make error.cpp.exec',
                                              output='g++ --std=c++11 error.cpp -o error.cpp.exec\n',
                                              error=False,
                                              status=RunStatus.SUCCESS,
                                              truncated=False,
                                              truncated_after=10000),
                                   TestResult(command='./error.cpp.exec',
                                              output="Command '['./error.cpp.exec']' returned non-zero exit status 1.",
                                              error=True,
                                              status=RunStatus.CALLED_PROCESS_ERROR,
                                              truncated=False,
                                              truncated_after=10000)]


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'test_file'))
def test_test_file_truncated(datafiles):
    spec = SpecFile(file_name='chatty.cpp',
                    compile_commands=[],
                    test_commands=['make chatty.cpp.exec', '$@.exec'],
                    options=FileOptions(truncate_output=180))  # 5 lines * 36 chars
    result = FileResult(file_name='chatty.cpp')

    with chdir(str(datafiles)):
        test_file(file_spec=spec, file_results=result, supporting_dir='', interact=False)

    assert result.test_results == [TestResult(command='make chatty.cpp.exec',
                                              output='g++ --std=c++11 chatty.cpp -o chatty.cpp.exec\n',
                                              error=False,
                                              status=RunStatus.SUCCESS,
                                              truncated=False,
                                              truncated_after=180),
                                   TestResult(command='./chatty.cpp.exec',
                                              output="Hi, I'm chatty, I like to say a lot\n"
                                                     "Hi, I'm chatty, I like to say a lot\n"
                                                     "Hi, I'm chatty, I like to say a lot\n"
                                                     "Hi, I'm chatty, I like to say a lot\n"
                                                     "Hi, I'm chatty, I like to say a lot\n",
                                              error=False,
                                              status=RunStatus.SUCCESS,
                                              truncated=True,
                                              truncated_after=180)]


# ----------------------------- process_file -----------------------------

def test_process_file_fail_get(tmpdir):
    spec = SpecFile(file_name='not_a_file.txt',
                    compile_commands=['compile me', 'and again'],
                    test_commands=['a test', 'another test'],
                    options=FileOptions())

    with tmpdir.as_cwd():
        touch('other_file.txt')
        result = process_file(file_spec=spec,
                              supporting_dir='.',
                              interact=False,
                              skip_web_compile=False)

    assert result.file_name == 'not_a_file.txt'
    assert not result.contents
    assert not result.compile_results
    assert not result.test_results
    assert result.file_missing is True
    assert not result.last_modified
    assert result.other_files == ['other_file.txt']
    assert result.optional is False
    assert result.compile_optional is False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'process_file'))
def test_process_file_fail_compile(datafiles):
    spec = SpecFile(file_name='bad.cpp',
                    compile_commands=['g++ --std=c++11 $@ -o $@.exec'],
                    test_commands=['a test', 'another test'],
                    options=FileOptions())

    with chdir(str(datafiles)):
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        git('add', 'bad.cpp')
        git('commit', '-m', '"Add file"', '--date="Tue Apr 21 12:28:03 2020 -0500"')

        result = process_file(file_spec=spec,
                              supporting_dir='.',
                              interact=False,
                              skip_web_compile=False)

    assert result.file_name == 'bad.cpp'
    assert '\n' + result.contents == textwrap.dedent('''
        #include <iostream>\n
        using namespace std;\n
        int main() {
            cout << "Hello" << endl;
            return 0;
        ''')

    for c_result in result.compile_results:
        c_result.output = c_result.output.replace('\r\n', '\n')

    assert result.compile_results == [CompileResult(command='g++ --std=c++11 ./bad.cpp -o ./bad.cpp.exec',
                                                    output='./bad.cpp: In function ‘int main()’:\n'
                                                           './bad.cpp:7:13: error: expected ‘}’ at end of input\n'
                                                           '     return 0;\n'
                                                           '             ^\n',
                                                    status=RunStatus.CALLED_PROCESS_ERROR)]
    assert not result.test_results
    assert result.file_missing is False
    assert result.last_modified == 'Tue Apr 21 12:28:03 2020 -0500'
    assert not result.other_files
    assert result.optional is False
    assert result.compile_optional is False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'process_file'))
def test_process_file_success(datafiles):
    spec = SpecFile(file_name='good.cpp',
                    compile_commands=['g++ --std=c++11 $@ -o $@.exec'],
                    test_commands=['$@.exec'],
                    options=FileOptions())

    with chdir(str(datafiles)):
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        git('add', 'good.cpp')
        git('commit', '-m', '"Add file"', '--date="Tue Apr 21 12:28:03 2020 -0500"')

        result = process_file(file_spec=spec,
                              supporting_dir='.',
                              interact=False,
                              skip_web_compile=False)

    assert result.file_name == 'good.cpp'
    assert '\n' + result.contents == textwrap.dedent('''
        #include <iostream>\n
        using namespace std;\n
        int main() {
            cout << "Hello" << endl;
            return 0;
        }
        ''')
    assert result.compile_results == [CompileResult(command='g++ --std=c++11 ./good.cpp -o ./good.cpp.exec',
                                                    output='',
                                                    status=RunStatus.SUCCESS)]
    assert result.test_results == [TestResult(command='./good.cpp.exec',
                                              output='Hello\n',
                                              error=False,
                                              status=RunStatus.SUCCESS,
                                              truncated=False,
                                              truncated_after=10000)]
    assert result.file_missing is False
    assert result.last_modified == 'Tue Apr 21 12:28:03 2020 -0500'
    assert not result.other_files
    assert result.optional is False
    assert result.compile_optional is False


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'process_file'))
def test_process_file_skip_web(datafiles):
    spec = SpecFile(file_name='good.cpp',
                    compile_commands=['g++ --std=c++11 $@ -o $@.exec'],
                    test_commands=['$@.exec'],
                    options=FileOptions(web_file=True))

    with chdir(str(datafiles)):
        git('init')
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        git('add', 'good.cpp')
        git('commit', '-m', '"Add file"', '--date="Tue Apr 21 12:28:03 2020 -0500"')

        result = process_file(file_spec=spec,
                              supporting_dir='.',
                              interact=False,
                              skip_web_compile=True)

    assert result.file_name == 'good.cpp'
    assert '\n' + result.contents == textwrap.dedent('''
        #include <iostream>\n
        using namespace std;\n
        int main() {
            cout << "Hello" << endl;
            return 0;
        }
        ''')
    assert not result.compile_results
    assert not result.test_results
    assert result.file_missing is False
    assert result.last_modified == 'Tue Apr 21 12:28:03 2020 -0500'
    assert not result.other_files
    assert result.optional is False
    assert result.compile_optional is False
