import logging
from os import path
from stograde.common import chdir
from stograde.process_assignment import process_assignment
from stograde.process_assignment.Record_Result import RecordResult


def record(student, *, specs, assignments, basedir, debug, interact, ci, skip_web_compile):
    results = []
    if not assignments:
        return results

    directory = student if not ci else '.'
    with chdir(directory):
        for spec in specs:
            logging.debug("Recording {}'s {}".format(student, spec.id))
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
