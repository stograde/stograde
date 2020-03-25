from dataclasses import dataclass

from .assignment_status import AssignmentStatus


@dataclass
class AnalysisResult:
    """The result of analyzing an assignment for a student"""
    status: AssignmentStatus  # The submission status of the assignment
