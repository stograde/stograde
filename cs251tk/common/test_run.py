from .run import run


def test_run():
    status, result = run(['echo', 'hi'])
    assert status == 'success'
    assert result == 'hi\n'


def test_run_stdin():
    status, result = run(['cat'], input_data=b'hello')
    assert status == 'success'
    assert result == 'hello'


def test_run_timeout():
    status, result = run(['sleep', '1'], timeout=0.5)
    assert status == 'timed out after 0.5 seconds'
    assert result == "Command '['sleep', '1']' timed out after 0.5 seconds"


def test_run_not_found():
    status, result = run(['notfound'])
    assert status == 'not found'
    assert result == "[Errno 2] No such file or directory: 'notfound'"
