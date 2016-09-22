from cs251tk.student import remove
from cs251tk.student import clone
from cs251tk.student import checkout_ref
from cs251tk.student import record
from cs251tk.student import analyze


def process_student(student, ref, stogit, specs, basedir):
    if not specs:
        raise Exception('`specs` should not be none')
    if not basedir:
        raise Exception('`basedir` should not be none')

    clone(student, baseurl=stogit)

    try:
        checkout_ref(student, ref=ref)

        record = discover_assignments(ref)

        recordings = record(student, specs, record=args['record'], basedir=basedir)
        analysis = analyze(student, specs, no_check=False)

        remove(student)

        return analysis, recordings

    except Exception as err:
        return {'username': student, 'error': err}, []

