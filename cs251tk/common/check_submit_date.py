import os
import logging
from dateutil.parser import parse
from .chdir import chdir
from .run import run


def check_dates(spec_id, username, spec, basedir):
    """ Port of the CheckDates program from C++
        Finds the first submission date for an assignment
        by comparing first commits for all files in the spec
        and returning the earliest """

    basedir = os.path.join(basedir, 'students', username, spec_id)
    dates = []

    with chdir(basedir):
        for file in spec['files']:

            # Run a git log on each file with earliest commits listed first
            try:
                status, res, _ = run(['git', 'log', '--reverse', '--pretty=format:%ad', '--date=iso8601', '--',
                                      os.path.join(basedir, file['filename'])])
            except Exception as e:
                logging.debug("CHECK_DATES Exception: {}".format(e))
                return "ERROR"

            # If we didn't get an error and got an output, add date to array
            if status == 'success' and res:
                # Parse the first line
                dates.append(parse(res.splitlines()[0]))

    # Return earliest date as a string with the format mm/dd/yyyy hh:mm:ss
    if not dates:
        return "ERROR"

    return min(dates).strftime("%x %X")
