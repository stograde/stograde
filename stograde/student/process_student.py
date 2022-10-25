from typing import List, TYPE_CHECKING

from .analyze_student import analyze_student
from .record_student import record_student
from ..student import checkout_date, clone_student
from ..student.pull import pull
from ..student.remove import remove
from ..student.reset import reset
from ..student.stash import stash
from ..student.student_result import StudentResult
from ..toolkit import global_vars

if TYPE_CHECKING:
    from ..specs.spec import Spec


def process_student(
        student: str,
        *,
        analyze: bool,
        basedir: str,
        branch: str,
        clean: bool,
        date: str,
        interact: bool,
        record: bool,
        skip_branch_check: bool,
        skip_repo_update: bool,
        skip_web_compile: bool,
        specs: List['Spec'],
        stogit_url: str
) -> StudentResult:
    try:
        prepare_student(student,
                        stogit_url,
                        branch,
                        do_clean=clean,
                        do_clone=not global_vars.CI and not skip_repo_update,
                        do_pull=not global_vars.CI and not skip_repo_update,
                        do_checkout=not global_vars.CI,
                        date=date)

        student_result = StudentResult(name=student)

        if record:
            record_student(student=student_result, specs=specs, basedir=basedir,
                           interact=interact, skip_web_compile=skip_web_compile)

        if analyze:
            analyze_student(student=student_result, specs=specs, check_for_branches=not skip_branch_check)

        if student_result.unmerged_branches:
            for result in student_result.results:
                result.warnings.unmerged_branches = student_result.unmerged_branches

        if date:
            reset(student)

        return student_result

    except Exception as err:
        if global_vars.DEBUG:
            raise err
        else:
            return StudentResult(name=student, error=str(err))


def prepare_student(student: str,
                    stogit_url: str,
                    branch: str,
                    do_clean: bool,
                    do_clone: bool,
                    do_pull: bool,
                    do_checkout: bool,
                    date: str = '') -> str:
    if do_clean:
        remove(student)
    if do_clone:
        clone_student(student, base_url=stogit_url)
    if do_pull:
        stash(student)
        pull(student, branch=branch)
    if do_checkout:
        checkout_date(student, branch=branch, date=date)

    return student
