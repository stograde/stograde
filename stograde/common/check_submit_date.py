from typing import TYPE_CHECKING

from dateutil.parser import parse
import os
import logging

from .run import run

if TYPE_CHECKING:
    from ..specs.spec import Spec


def check_dates(spec: 'Spec', cwd: str) -> str:
    """ Port of the CheckDates program from C++
    Finds the first submission date for an assignment
    by comparing first commits for all files in the spec
    and returning the earliest date
    """

    dates = []

    for file in spec.files:
        # Run a git log on each file with earliest commits listed first
        try:
            status, res, _ = run(['git', 'log', '--reverse', '--pretty=format:%ad', '--date=iso8601', '--',
                                  os.path.join(cwd, file.file_name)])
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
