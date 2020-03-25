from dataclasses import dataclass


@dataclass
class TestResult:
    command: str
    output: str
    error: bool
    status: str
    truncated: bool = False
    truncated_after: int = 0
