from typing import Dict, List, TYPE_CHECKING

from . import record_student, analyze_student
from ..student import checkout_date, clone_student, pull, remove, reset, stash
from ..student.student_result import StudentResult
from ..toolkit.global_vars import CI, DEBUG

if TYPE_CHECKING:
    from ..specs.spec import Spec


def process_student(
        student: str,
        *,
        analyze: bool,
        basedir: str,
        clean: bool,
        date: str,
        interact: bool,
        record: bool,
        skip_branch_check: bool,
        skip_repo_update: bool,
        skip_web_compile: bool,
        specs: Dict[str, 'Spec'],
        stogit_url: str
) -> StudentResult:
    assignments: List[str] = list(specs.keys())

    try:
        prepare_student(student,
                        stogit_url,
                        do_clean=clean,
                        do_clone=not CI and not skip_repo_update,
                        do_pull=not CI and not skip_repo_update,
                        do_checkout=not CI,
                        date=date)

        student_result = StudentResult(name=student)

        if record:
            record_student(student=student_result, specs=specs, assignments=assignments, basedir=basedir,
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
        if DEBUG:
            raise err
        else:
            return StudentResult(name=student, error=str(err))


def prepare_student(student: str,
                    stogit_url: str,
                    do_clean: bool,
                    do_clone: bool,
                    do_pull: bool,
                    do_checkout: bool,
                    date: str = ''):
    if do_clean:
        remove(student)
    if do_clone:
        clone_student(student, base_url=stogit_url)
    if do_pull:
        stash(student)
        pull(student)
    if do_checkout:
        checkout_date(student, date=date)


def prepare_student_repo(student: str,
                         stogit_url: str,
                         do_clean: bool,
                         do_clone: bool,
                         do_pull: bool,
                         do_checkout: bool,
                         date: str = '') -> str:
    prepare_student(student,
                    stogit_url,
                    do_clean,
                    do_clone,
                    do_pull,
                    do_checkout,
                    date)

    return student
