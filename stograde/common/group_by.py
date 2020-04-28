from itertools import groupby
from types import LambdaType
from typing import Any, Generator, List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..process_assignment.record_result import RecordResult

__all__ = ['group_by']


def group_by(iterable: List['RecordResult'],
             predicate: LambdaType) -> Generator[Tuple[Any, List['RecordResult']], None, None]:
    """Group an iterable by a predicate function"""
    sorted_iterable = sorted(iterable, key=predicate)
    grouped = groupby(sorted_iterable, key=predicate)
    for k, v in grouped:
        yield k, list(v)
