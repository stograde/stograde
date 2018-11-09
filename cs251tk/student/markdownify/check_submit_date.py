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
            _, res, _ = run(['git', 'log', '--reverse', '--pretty=format:%ad', '--date=iso8601',
                             os.path.join(basedir, file['filename'])])

            # If we didn't get an error, add date to array
            if res[0] is not 'f':
                # Parse the first line
                dates.append(parse(res.splitlines()[0]))

    # Sort dates earliest to latest
    dates.sort()

    # Return earliest date as a string with the format mm/dd/yyyy hh:mm:ss
    return dates[0].strftime("%x %X")
