from dataclasses import dataclass, field
from typing import List


@dataclass
class SubmissionWarnings:
    """Track any warnings about the assignment"""
    assignment_missing: bool = False  # No assignment submission could be found
    recording_err: str = None  # Something raised an error during recording
    unmerged_branches: List[str] = field(default_factory=list)  # There are unmerged branches that might have more code
