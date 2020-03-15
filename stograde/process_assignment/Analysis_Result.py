from dataclasses import dataclass

from stograde.process_assignment.Assignment_Status import AssignmentStatus


@dataclass
class AnalysisResult:
    status: AssignmentStatus
