from enum import Enum, auto


class AssignmentStatus(Enum):
    SUCCESS = auto()
    PARTIAL = auto()
    MISSING = auto()
