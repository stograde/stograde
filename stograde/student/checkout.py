import logging
from typing import Optional

from ..common import chdir, run


def checkout_date(student: str, date: Optional[str] = None):
    if date:
        logging.debug("Checking out commits in {}'s repository before {}".format(student, date))
        with chdir(student):
            _, rev, _ = run(['git', 'rev-list', '-n', '1', '--before="{} 18:00"'.format(date), 'master'])
        checkout_ref(student, rev.rstrip())


def checkout_ref(student: str, ref: str):
    with chdir(student):
        run(['git', 'checkout', ref, '--force', '--quiet'])
