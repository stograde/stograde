from .run import run


def test_run():
    status, result = run(['echo', 'hi'])
    assert status == 'success'
    assert result == 'hi\n'
