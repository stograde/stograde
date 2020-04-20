from dateutil.parser import parse
import os
from typing import TYPE_CHECKING

from .run import run
from .run_status import RunStatus

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
        status, res, _ = run(['git', 'log', '--reverse', '--pretty=format:%ad', '--date=iso8601', '--',
                              os.path.join(cwd, file.file_name)])

        if status is RunStatus.SUCCESS and res:
            # If we didn't get an error and got an output, add date to array
            # Note: a missing file will still return a success code but have no output
            dates.append(parse(res.splitlines()[0]))

    if dates:
        # Return earliest date as a string with the format mm/dd/yyyy hh:mm:ss
        return min(dates).strftime('%x %X')
    else:
        # If we couldn't find any dates, say so
        return 'ERROR: NO DATES'
