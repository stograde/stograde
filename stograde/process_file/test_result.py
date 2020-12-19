from dataclasses import dataclass
from typing import Optional

from ..common.run_status import RunStatus


@dataclass
class TestResult:
    """Result from testing an assignment file"""
    command: str  # Command used to test
    output: str  # Output from the test
    error: bool  # Did the command return an error code
    status: RunStatus  # Status from running the test
    truncated_after: Optional[int] = None  # How much was it truncated
