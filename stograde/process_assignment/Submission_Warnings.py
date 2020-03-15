from dataclasses import dataclass


@dataclass
class SubmissionWarnings:
    assignment_missing: bool = False
    recording_err: str = None
