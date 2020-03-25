from enum import auto, Enum


class AssignmentStatus(Enum):
    """The completeness of the assignment"""
    SUCCESS = auto()  # All required files are present
    PARTIAL = auto()  # Some files are missing
    MISSING = auto()  # No files are present
