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
    assert result == "[Errno 2] No such file or directory: 'notfound': 'notfound'"
    assert again is False
