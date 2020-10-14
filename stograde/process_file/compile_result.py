from dataclasses import dataclass
from typing import Optional

from ..common.run_status import RunStatus


@dataclass
class CompileResult:
    """Result from compiling an assignment file"""
    command: str  # Command used to compile
    output: str  # Output from running the command
    status: RunStatus  # Status from running the command
    truncated_after: Optional[int] = None  # How much was it truncated
