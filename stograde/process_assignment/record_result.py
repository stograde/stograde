from dataclasses import dataclass, field
from typing import List

from .submission_warnings import SubmissionWarnings
from ..process_file.file_result import FileResult


@dataclass
class RecordResult:
    spec_id: str
    student: str
    first_submission: str = ''
    warnings: SubmissionWarnings = field(default_factory=SubmissionWarnings)
    file_results: List[FileResult] = field(default_factory=list)

