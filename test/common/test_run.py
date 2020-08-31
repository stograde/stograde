import sys
from subprocess import CompletedProcess
from unittest import mock

from stograde.common.run import run
from stograde.common.run_status import RunStatus


def test_run():
    status, result, again = run(['echo', 'hi'])
    assert status == RunStatus.SUCCESS
    assert result == 'hi\n'
    assert again is False


def test_run_stdin():
    status, result, again = run(['cat'], input_data=b'hello')
    assert status == RunStatus.SUCCESS
    assert result == 'hello'
    assert again is False


def test_run_timeout():
    status, result, again = run(['sleep', '1'], timeout=0.5)
    assert status == RunStatus.TIMEOUT_EXPIRED
    assert result == "Command '['sleep', '1']' timed out after 0.5 seconds"
    assert again is False


def test_run_not_found():
    status, result, again = run(['notfound'])
    assert status == RunStatus.FILE_NOT_FOUND
    if sys.version_info.minor < 8:
        assert result == "[Errno 2] No such file or directory: 'notfound': 'notfound'"
    else:
        assert result == "[Errno 2] No such file or directory: 'notfound'"
    assert again is False


def test_run_process_lookup_error():
    with mock.patch('subprocess.run', side_effect=ProcessLookupError('Lookup error')):
        status, result, again = run(['error'])
    assert status == RunStatus.PROCESS_LOOKUP_ERROR
    assert result == 'Lookup error'
    assert again is False


def test_run_unicode_decode_error():
    with mock.patch('subprocess.run',
                    return_value=CompletedProcess(['echo', 'ü'], 0, b'\x81\n')):
        status, result, again = run(['echo', 'ü'])
    assert status == RunStatus.SUCCESS
    assert result == 'ü\n'
    assert again is False


def test_run_interactive_y(capsys):
    with mock.patch('builtins.input', return_value='y'):
        status, result, again = run(['echo', 'a'], interact=True)
    assert status == RunStatus.SUCCESS
    assert result == 'a\r\n'
    assert again is True

    out, _ = capsys.readouterr()

    assert out == ("Recording ['echo', 'a']. Send EOF (^D) to end.\n\n\n"
                   'Submission recording completed.\n')


def test_run_interactive_n(capsys):
    with mock.patch('builtins.input', return_value='n'):
        status, result, again = run(['echo', 'a'], interact=True)
    assert status == RunStatus.SUCCESS
    assert result == 'a\r\n'
    assert again is False

    out, _ = capsys.readouterr()

    assert out == ("Recording ['echo', 'a']. Send EOF (^D) to end.\n\n\n"
                   'Submission recording completed.\n')


def test_run_interactive_unicode_decode_error(capsys):
    with mock.patch('builtins.input', return_value='n'):
        status, result, again = run(['echo', b'\x81'], interact=True)
    assert status == RunStatus.SUCCESS
    assert result == 'ü\r\n'
    assert again is False

    out, _ = capsys.readouterr()

    assert out == ("Recording ['echo', b'\\x81']. Send EOF (^D) to end.\n\n\n"
                   'Submission recording completed.\n')
