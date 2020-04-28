import datetime
import os
import re
import sys

from ..common import chdir, run
from ..common.run_status import RunStatus
from ..specs.spec_repos import get_course_from_spec_url, default_course

COURSE_REGEX = re.compile(r'^([\w]{2,3}/[sf]\d\d)$')


def compute_stogit_url(*,
                       stogit: str,
                       course: str,
                       _now: datetime.date = datetime.date.today()) -> str:
    """calculate a default stogit URL, or use the specified one"""
    if stogit:
        return stogit
    elif re.match(COURSE_REGEX, course):
        return 'git@stogit.cs.stolaf.edu:{}'.format(course)
    else:
        if not course:
            course = get_course_from_specs()
        semester = 's' if _now.month < 7 else 'f'
        year = str(_now.year)[2:]
        return 'git@stogit.cs.stolaf.edu:{}/{}{}'.format(course.lower(), semester, year)


def get_course_from_specs() -> str:
    if not os.path.exists('data'):
        print('Unable to determine course from specs: no data directory', file=sys.stderr)
        sys.exit(1)

    with chdir('data'):
        status, res, _ = run(['git', 'config', '--get', 'remote.origin.url'])
        if status != RunStatus.SUCCESS:
            print('Could not get URL from data directory: {}'.format(res), file=sys.stderr)
            return default_course()
        else:
            return get_course_from_spec_url(res.strip())
