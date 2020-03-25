from collections import OrderedDict
from dataclasses import dataclass, field
from typing import List, Dict

from stograde.process_assignment.assignment_status import AssignmentStatus
from stograde.process_assignment.record_result import RecordResult


@dataclass
class StudentResult:
    name: str
    results: List[RecordResult] = field(default_factory=list)
    homeworks: Dict[str, AssignmentStatus] = field(default_factory=OrderedDict)
    labs: Dict[str, AssignmentStatus] = field(default_factory=OrderedDict)
    worksheets: Dict[str, AssignmentStatus] = field(default_factory=OrderedDict)
    unmerged_branches: List[str] = field(default_factory=list)
    error: str = ''

    def assignments(self) -> Dict[str, AssignmentStatus]:
        assignments = {}
        assignments.update(self.homeworks)
        assignments.update(self.labs)
        assignments.update(self.worksheets)
        return assignments
