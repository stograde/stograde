from enum import auto, Enum


class RunStatus(Enum):
    SUCCESS = auto()
    CALLED_PROCESS_ERROR = auto()
    FILE_NOT_FOUND = auto()
    PROCESS_LOOKUP_ERROR = auto()
    TIMEOUT_EXPIRED = auto()
