from cs251tk.student import remove
from cs251tk.student import clone_student
from cs251tk.student import stash
from cs251tk.student import pull
from cs251tk.student import checkout_date
from cs251tk.student import record
from cs251tk.student import reset
from cs251tk.student import analyze
import logging


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
    if debug:
        logging.debug("Cloning    {}'s repository".format(student))
        # logging.debug("{} \tClone".format(student))
    clone_student(student, baseurl=stogit_url)

    try:
        if debug:
            logging.debug("Stashing   {}'s repository".format(student))
            # logging.debug("{} \tStash".format(student))
        stash(student, no_update=no_update)

        if debug:
            logging.debug("Pulling    {}'s repository".format(student))
            # logging.debug("{} \tPull")
        pull(student, no_update=no_update)

        if debug and date:
            logging.debug("Checking out commits in {}'s repository before {}".format(student, date))
        checkout_date(student, date=date)

        # if debug:
        #     logging.debug("Recording  {}'s assignments".format(student))
        recordings = record(student, specs=specs, to_record=assignments, basedir=basedir, debug=debug, interact=interact)
        if debug:
            logging.debug("Analyzing  {}'s assignments".format(student))
        analysis = analyze(student, specs, check_for_branches=not no_check)

        if date:
            reset(student)

        return analysis, recordings

    except Exception as err:
        if debug:
            raise err
        return {'username': student, 'error': err}, []
