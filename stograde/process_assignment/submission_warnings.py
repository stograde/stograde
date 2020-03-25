from dataclasses import dataclass, field
from typing import List


@dataclass
class SubmissionWarnings:
    assignment_missing: bool = False
    recording_err: str = None
    unmerged_branches: List[str] = field(default_factory=list)
