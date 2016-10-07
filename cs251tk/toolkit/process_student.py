from cs251tk.student import remove
from cs251tk.student import clone_student
from cs251tk.student import stash
from cs251tk.student import pull
from cs251tk.student import checkout_date
from cs251tk.student import record
from cs251tk.student import reset
from cs251tk.student import analyze


def process_student(student, args=None, specs=None, basedir=None, debug=False):
    if not args:
        raise Exception('`args` should not be none')
    if not specs:
        raise Exception('`specs` should not be none')
    if not basedir:
        raise Exception('`basedir` should not be none')

    if args['clean']:
        remove(student)

    clone_student(student, baseurl=args['stogit'])

    try:
        stash(student, no_update=args['no_update'])
        pull(student, no_update=args['no_update'])

        checkout_date(student, date=args['date'])

        recordings = record(student, specs, to_record=args['record'], basedir=basedir, debug=debug)
        analysis = analyze(student, specs, check_for_branches=not args['no_check'])

        if args['date']:
            reset(student)

        return analysis, recordings

    except Exception as err:
        return {'username': student, 'error': err}, []
