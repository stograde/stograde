from enum import auto, Enum
import re
from typing import Tuple


class AssignmentType(Enum):
    HOMEWORK = auto()
    LAB = auto()
    WORKSHEET = auto()


def get_assignment_type(name: str) -> AssignmentType:
    kind, _ = parse_assignment_name(name)

    if kind == 'hw':
        return AssignmentType.HOMEWORK
    elif kind == 'lab':
        return AssignmentType.LAB
    elif kind == 'ws':
        return AssignmentType.WORKSHEET
    else:
        raise TypeError("Could not parse assignment type for {}".format(name))


def get_assignment_number(name: str) -> int:
    _, num = parse_assignment_name(name)
    return int(num)


def parse_assignment_name(name: str) -> Tuple[str, str]:
    matches = re.match(r'([a-zA-Z]+)(\d+)', name).groups()
    return matches[0], matches[1]

