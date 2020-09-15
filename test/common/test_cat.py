from stograde.common.cat import cat
from stograde.common.run_status import RunStatus


def test_cat(fs):
    filename = 'foo.txt'
    contents = 'insert a story here'
    fs.create_file(filename, contents=contents)

    result = cat(filename)
    assert result[0] == RunStatus.SUCCESS
    assert result[1] == contents


def test_cat_missing():
    result = cat('file.txt')
    assert result[0] == RunStatus.FILE_NOT_FOUND
    assert result[1] == ''
