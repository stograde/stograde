from .run import run


def test_run():
    status, result, again = run(['echo', 'hi'])
    assert status == 'success'
    assert result == 'hi\n'
    assert again == False


def test_run_stdin():
    status, result, again = run(['cat'], input_data=b'hello')
    assert status == 'success'
    assert result == 'hello'
    assert again == False


def test_run_timeout():
    status, result, again = run(['sleep', '1'], timeout=0.5)
    assert status == 'timed out after 0.5 seconds'
    assert result == "Command '['sleep', '1']' timed out after 0.5 seconds"
    assert again == False


def test_run_not_found():
    status, result, again = run(['notfound'])
    assert status == 'not found'
    assert result == "[Errno 2] No such file or directory: 'notfound'"
    assert again == False
