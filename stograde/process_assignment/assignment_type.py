from enum import auto, Enum
import re
from typing import Tuple


class AssignmentType(Enum):
    """The type of assignment"""
    HOMEWORK = auto()
    LAB = auto()
    WORKSHEET = auto()


def get_assignment_type(name: str) -> AssignmentType:
    """Determine the assignment type from a string

    Throws a ValueError if name is not a valid assignment type"""
    kind, _ = parse_assignment_name(name)

    if kind == 'hw':
        return AssignmentType.HOMEWORK
    elif kind == 'lab':
        return AssignmentType.LAB
    elif kind == 'ws':
        return AssignmentType.WORKSHEET
    else:
        raise ValueError("Could not parse assignment type for {}".format(name))


def get_assignment_number(name: str) -> int:
    """Returns the number associated with the assignment"""
    _, num = parse_assignment_name(name)
    return int(num)


def parse_assignment_name(name: str) -> Tuple[str, str]:
    """Splits an assignment id into its type and number"""
    matches = re.match(r'([a-zA-Z]+)(\d+)', name).groups()
    return matches[0], matches[1]
