import os
from dateutil.parser import parse
from ...common import run, chdir


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
            _, res, _ = run(['git', 'log', '--reverse',
                             os.path.join(basedir, file['filename'])])

            # If we didn't get an error, add date to array
            if res[0] is not 'f':
                # Parse the third line, without the first 7 and last 6 characters, for a date to add
                dates.append(parse(res.splitlines()[2][8:][:-6]))

    # Sort dates earliest to latest
    dates.sort()

    # Return earliest date as a string with the format mm/dd/yyyy hh:mm:ss
    return dates[0].strftime("%x %X")
