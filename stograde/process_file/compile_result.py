from dataclasses import dataclass

from ..common.run_status import RunStatus


@dataclass
class CompileResult:
    """Result from compiling an assignment file"""
    command: str  # Command used to compile
    output: str     # Output from running the command
    status: RunStatus
