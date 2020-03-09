import os
import re
import sys

from stograde.common import run, chdir
from stograde.toolkit.download_specs import SPEC_URLS

COURSE_REGEX = re.compile(r'^([\w]{2,3}/[sf]\d\d)$')


def compute_stogit_url(*, stogit, course, _now, **kwargs) -> str:
    """calculate a default stogit URL, or use the specified one"""
    if stogit:
        return stogit
    elif re.match(COURSE_REGEX, course):
        return 'git@stogit.cs.stolaf.edu:{}'.format(course)
    else:
        if not course:
            course = get_course_from_specs()
            print('Course {} inferred from specs'.format(course.upper()))
        semester = 's' if _now.month < 7 else 'f'
        year = str(_now.year)[2:]
        return 'git@stogit.cs.stolaf.edu:{}/{}{}'.format(course, semester, year)


def get_course_from_specs():
    if not os.path.exists("data"):
        print('Cannot compute course from specs', file=sys.stderr)
        sys.exit(1)

    with chdir('./data'):
        _, res, _ = run(['git', 'config', '--get', 'remote.origin.url'])
        try:
            course = SPEC_URLS.inverse[res.rstrip()]
        except KeyError:
            course = 'sd'     # default to SD as last resort
        finally:
            return course
