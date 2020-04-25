"""Given a spec, assuming we're in the homework folder, run the spec against the folder"""

import os
from typing import TYPE_CHECKING

from .record_result import RecordResult
from .submission_warnings import SubmissionWarnings
from .supporting import import_supporting, remove_supporting
from ..common import get_assignment_first_submit_time
from ..process_file import process_file
from ..toolkit import global_vars

if TYPE_CHECKING:
    from ..specs.spec import Spec
    from ..student.student_result import StudentResult


def process_assignment(*,
                       student: 'StudentResult',
                       spec: 'Spec',
                       basedir: str,
                       interact: bool,
                       skip_web_compile: bool) -> RecordResult:
    """Run a spec against the current folder"""
    cwd = os.getcwd()
    try:
        first_submit = ''

        if not global_vars.CI:
            first_submit = get_assignment_first_submit_time(spec, cwd)

        result = RecordResult(spec_id=spec.id,
                              first_submission=first_submit,
                              student=student.name)

        # prepare the current folder
        supporting_dir, written_files = import_supporting(spec=spec,
                                                          basedir=basedir)

        # process the assignment
        for file_spec in spec.files:
            file_result = process_file(file_spec=file_spec,
                                       cwd=cwd,
                                       supporting_dir=supporting_dir,
                                       interact=interact,
                                       skip_web_compile=skip_web_compile)
            result.file_results.append(file_result)

        # now we remove any compiled binaries
        remove_execs(spec)

        # and we remove any supporting files
        remove_supporting(written_files)

        return result

    except Exception as err:
        if global_vars.DEBUG:
            raise err
        else:
            return RecordResult(student=student.name,
                                spec_id=spec.id,
                                warnings=SubmissionWarnings(recording_err=str(err)))


def remove_execs(spec: 'Spec'):
    """Remove executable files (identified by a .exec extension)"""
    try:
        for file in spec.files:
            os.remove('{}.exec'.format(file.file_name))
    except FileNotFoundError:
        pass
