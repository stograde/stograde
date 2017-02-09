from inspect import isgenerator
from .group_by import group_by


def test_group_by():
    assert isgenerator(group_by([1, 2, 3], lambda s: s % 2 == 0))
    assert dict(group_by(['1', '2', '3'], lambda s: s.isdigit())) == {True: ['1', '2', '3']}
    assert dict(group_by(
        [{'a': 1}, {'a': 2}, {'a': 1}],
        lambda i: i['a'])) == {1: [{'a': 1}, {'a': 1}], 2: [{'a': 2}]}
