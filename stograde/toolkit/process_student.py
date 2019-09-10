from stograde.student import remove
from stograde.student import clone_student
from stograde.student import stash
from stograde.student import pull
from stograde.student import checkout_date
from stograde.student import record
from stograde.student import reset
from stograde.student import analyze


def process_student(
        student,
        *,
        assignments,
        basedir,
        ci,
        clean,
        date,
        debug,
        interact,
        no_check,
        no_update,
        specs,
        skip_web_compile,
        stogit_url
):
    if clean:
        remove(student)
    if not ci:
        clone_student(student, baseurl=stogit_url)

    try:
        if not ci:
            stash(student, no_update=no_update)
            pull(student, no_update=no_update)

            checkout_date(student, date=date)

        recordings = record(student, specs=specs, to_record=assignments, basedir=basedir, debug=debug,
                            interact=interact, ci=ci, skip_web_compile=skip_web_compile)
        analysis = analyze(student, specs, check_for_branches=not no_check, ci=ci)

        if date:
            reset(student)

        return analysis, recordings

    except Exception as err:
        if debug:
            raise err
        return {'username': student, 'error': err}, []
