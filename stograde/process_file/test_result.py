from dataclasses import dataclass

from ..common.run_status import RunStatus


@dataclass
class TestResult:
    """Result from testing an assignment file"""
    command: str  # Command used to test
    output: str  # Output from the test
    error: bool  # Did the command return an error code
    status: RunStatus  # Status of the test
    truncated: bool = False  # Was the output truncated
    truncated_after: int = 0  # How much was it truncated
