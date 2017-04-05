from inspect import isgenerator
from .flatten import flatten


def test_flatten():
    assert isgenerator(flatten([]))
    assert list(flatten([1])) != [[1]]

    assert list(flatten([[]])) == []
    assert list(flatten([1, [2], [3]])) == [1, 2, 3]
    assert list(flatten([1, [2, 3], [[4]]])) == [1, 2, 3, 4]
