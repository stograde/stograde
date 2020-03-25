from dataclasses import dataclass, field
from typing import List

from .submission_warnings import SubmissionWarnings
from ..process_file.file_result import FileResult


@dataclass
class RecordResult:
    """The results of testing a student's submission for an assignment"""
    spec_id: str  # The spec being tested against
    student: str  # The student's username
    first_submission: str = ''  # The first commit of this assignment's files
    warnings: SubmissionWarnings = field(default_factory=SubmissionWarnings)  # Any warnings about the assignment
    file_results: List[FileResult] = field(default_factory=list)  # The results from each individual file
