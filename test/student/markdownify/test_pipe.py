from stograde.student.markdownify.pipe import pipe, expand_chunk, process_chunk


def test_expand_chunk(fs):
    fs.create_file('file1')
    fs.create_file('file2')

    assert expand_chunk('ls') == ['ls']
    assert sorted(expand_chunk('file*')) == sorted(['file1', 'file2'])


def test_process_chunk(fs):
    fs.create_file('file1')
    fs.create_file('file2')

    assert process_chunk('echo Hawken \n 26') == ['echo', 'Hawken', '26']


def test_pipe():
    assert pipe('echo hi | cat') == (['cat'], b'hi\n')
