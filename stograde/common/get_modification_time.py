import os
from typing import TYPE_CHECKING, Tuple

from .modification_time import ModificationTime
from .run import run

if TYPE_CHECKING:
    from ..specs.spec import Spec


def get_modification_time(file_name: str,
                          cwd: str,
                          modification: 'ModificationTime' = ModificationTime.LATEST) -> Tuple[str, str]:
    """Get the modification time for a file, either first or latest, based on the modification argument"""

    if not os.path.exists(os.path.join(cwd, file_name)):
        return '', ''

    # We can't use -n 1 here because that runs before --reverse
    # which would make this useless for finding the first date
    command = ['git', 'log', '--pretty=format:%ad']
    command_file = ['--', os.path.join(cwd, file_name)]
    if modification is ModificationTime.FIRST:
        command += ['--reverse']

    _, date, _ = run(command + command_file)
    _, iso_date, _ = run(command + ['--date=iso8601'] + command_file)
    return date.splitlines()[0], iso_date.splitlines()[0]


def get_assignment_first_submit_time(spec: 'Spec', cwd: str) -> str:
    """Get the first submission time for an assignment"""

    dates = {}

    for file in spec.files:
        # Run a git log on each file with earliest commits listed first
        date, iso_date = get_modification_time(file.file_name, cwd, ModificationTime.FIRST)

        if date and iso_date:
            dates[date] = iso_date

    if dates:
        # Return earliest date as a string with the format mm/dd/yyyy hh:mm:ss
        return min(dates.keys(), key=(lambda k: dates[k]))
    else:
        # If we couldn't find any dates, say so
        return 'ERROR: NO DATES'
