from enum import auto, Enum


class AssignmentStatus(Enum):
    SUCCESS = auto()
    PARTIAL = auto()
    MISSING = auto()
