import logging
from os import path
from typing import List, Dict

from ..common import chdir
from ..process_assignment.process_assignment import process_assignment
from ..process_assignment.record_result import RecordResult
from ..process_assignment.warning_unmerged_branches import find_unmerged_branches
from ..specs.spec import Spec
from ..student.student_result import StudentResult


def record(*,
           student: StudentResult,
           specs: Dict[str, Spec],
           assignments: List[str],
           basedir: str,
           debug: bool,
           interact: bool,
           ci: bool,
           skip_web_compile: bool):
    results = []
    if assignments:
        directory = student.name if not ci else '.'
        with chdir(directory):
            find_unmerged_branches(student)

            for _, spec in specs.items():
                if spec.id in assignments:
                    logging.debug("Recording {}'s {}".format(student.name, spec.id))
                    if path.exists(spec.id):
                        with chdir(spec.id):
                            assignment_result = process_assignment(student=student,
                                                                   spec=spec,
                                                                   basedir=basedir,
                                                                   debug=debug,
                                                                   interact=interact,
                                                                   ci=ci,
                                                                   skip_web_compile=skip_web_compile)
                    else:
                        assignment_result = RecordResult(spec_id=spec.id,
                                                         student=student.name)
                        assignment_result.warnings.assignment_missing = True

                    results.append(assignment_result)

    student.results = results
