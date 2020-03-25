from dataclasses import dataclass

from .assignment_status import AssignmentStatus


@dataclass
class AnalysisResult:
    status: AssignmentStatus
