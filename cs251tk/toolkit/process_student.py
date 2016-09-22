from cs251tk.student import remove
from cs251tk.student import clone
from cs251tk.student import stash
from cs251tk.student import pull
from cs251tk.student import checkout_day
from cs251tk.student import record
from cs251tk.student import reset
from cs251tk.student import analyze


def process_student(student, args=None, specs=None, basedir=None):
    if not args:
        raise Exception('`args` should not be none')
    if not specs:
        raise Exception('`specs` should not be none')
    if not basedir:
        raise Exception('`basedir` should not be none')

    if args['clean']:
        remove(student)

    clone(student, args['stogit'])

    try:
        stash(student, args)
        pull(student, args)

        checkout_day(student, args)

        recordings = record(student, specs, args, basedir)
        analysis = analyze(student, specs, args)

        reset(student, args)

        return analysis, recordings

    except Exception as err:
        return {'username': student, 'error': err}, []
