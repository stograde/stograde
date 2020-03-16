import logging
from os import path
from typing import List

from stograde.common import chdir
from stograde.process_assignment import process_assignment
from stograde.process_assignment.Record_Result import RecordResult
from stograde.specs import Spec
from stograde.student.Student_Result import StudentResult


def record(*,
           student: StudentResult,
           specs: List[Spec],
           assignments: List[str],
           basedir: str,
           debug: bool,
           interact: bool,
           ci: bool,
           skip_web_compile: bool):
    results = []
    if not assignments:
        return results

    directory = student.name if not ci else '.'
    with chdir(directory):
        for spec in specs:
            if spec.id in assignments:
                logging.debug("Recording {}'s {}".format(student.name, spec.id))
                if path.exists(spec.id):
                    with chdir(spec.id):
                        assignment_result = process_assignment(spec=spec,
                                                               basedir=basedir,
                                                               debug=debug,
                                                               interact=interact,
                                                               ci=ci,
                                                               skip_web_compile=skip_web_compile)
                else:
                    assignment_result = RecordResult(spec_id=spec.id)
                    assignment_result.warnings.assignment_missing = True

                results.append(assignment_result)

    return results
