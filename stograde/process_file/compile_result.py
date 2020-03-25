from dataclasses import dataclass


@dataclass
class CompileResult:
    command: str
    output: str
    status: str
