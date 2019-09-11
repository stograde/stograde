from itertools import groupby
__all__ = ['group_by']


def group_by(iterable, predicate):
    """Group an iterable by a predicate function"""
    sorted_iterable = sorted(iterable, key=predicate)
    grouped = groupby(sorted_iterable, key=predicate)
    for k, v in grouped:
        yield k, list(v)
