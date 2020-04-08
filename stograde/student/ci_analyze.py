import logging
import re
from typing import List, TYPE_CHECKING

from ..common.run_status import RunStatus

if TYPE_CHECKING:
    from ..student.student_result import StudentResult

LAB_REGEX = re.compile(r'^LAB', re.IGNORECASE)


def ci_analyze(student_results: List['StudentResult']) -> bool:
    passing = True
    for student_result in student_results:
        for result in student_result.results:
            try:
                for file in result.file_results:
                    # Alert student about any missing files
                    if file.file_missing and not file.optional:
                        logging.error("{}: File {} missing".format(result.spec_id, file.file_name))
                        if not re.match(LAB_REGEX, result.spec_id):
                            passing = False
                    else:
                        # Alert student about any compilation errors
                        for compilation in file.compile_results:
                            if compilation.status is not RunStatus.SUCCESS:
                                if file.compile_optional:
                                    logging.warning("{}: File {} compile error (This did not fail the build)"
                                                    .format(result.spec_id, file.file_name))
                                else:
                                    logging.error("{}: File {} compile error:\n\n\t{}"
                                                  .format(result.spec_id, file.file_name,
                                                          compilation.output.replace("\n", "\n\t")))
                                    if not re.match(LAB_REGEX, result.spec_id):
                                        passing = False
            except KeyError:
                logging.error("KeyError with {}".format(result.spec_id))
    return passing
