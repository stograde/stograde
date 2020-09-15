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


def get_assignment_number(name: str) -> int:
    """Returns the number associated with the assignment"""
    _, num = parse_assignment_name(name)
    return int(num)


def parse_assignment_name(name: str) -> Tuple[str, str]:
    """Splits an assignment id into its type and number"""
    matches = re.match(r'^(HW|LAB|WS)(\d+)$', name, re.IGNORECASE)
    if not matches:
        raise ValueError('Invalid assignment ID: {}'.format(name))
    else:
        match_groups = matches.groups()
        return match_groups[0], match_groups[1]
