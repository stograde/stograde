'''Check for program updates'''
import datetime
import yaml
from .run import run
from .helpers import warn
from .config import load_config, save_config
from update_checker import update_check

version = '2.0.5'


def check_for_updates():
    '''Check for updates from git, at most once an hour'''
    has_config, config = load_config()

    now = datetime.datetime.utcnow()
    one_hour = datetime.timedelta(hours=1)

    last_checked = config.get('last checked', now)

    # don't bother checking more than once an hour
    should_check = (now - last_checked) > one_hour
    if has_config and should_check:
        return

    update_check('cs251tk', version)

    config['last checked'] = last_checked

    save_config(config)
