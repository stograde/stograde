from cs251tk.student import remove
from cs251tk.student import clone_student
from cs251tk.student import stash
from cs251tk.student import pull
from cs251tk.student import checkout_date
from cs251tk.student import record
from cs251tk.student import reset
from cs251tk.student import analyze


def process_student(
    student,
    *,
    assignments,
    basedir,
    clean,
    date,
    debug,
    interact,
    no_check,
    no_update,
    specs,
    stogit_url
):
    if clean:
        remove(student)

    clone_student(student, baseurl=stogit_url)

    try:
        stash(student, no_update=no_update)
        pull(student, no_update=no_update)

        checkout_date(student, date=date)

        recordings = record(student, specs=specs, to_record=assignments, basedir=basedir, debug=debug, interact=interact)
        analysis = analyze(student, specs, check_for_branches=not no_check)

        if date:
            reset(student)

        return analysis, recordings

    except Exception as err:
        if debug:
            raise err
        return {'username': student, 'error': err}, []
