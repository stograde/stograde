'''Check for program updates'''
import datetime
import yaml
from .run import run
from .helpers import warn
from update_checker import update_check

version='2.0.5'


def check_for_updates():
    '''Check for updates from git, at most once an hour'''
    has_config = False
    with open('.cs251toolkitrc.yaml', 'a+', encoding='utf-8') as config_file:
        config_file.seek(0)
        try:
            contents = config_file.read()
        except OSError as err:
            warn(err)
            return

    if not contents:
        contents = ''

    try:
        config = yaml.safe_load(contents)
    except:
        config = {}

    if not config:
        config = {}
    else:
        has_config = True

    now = datetime.datetime.utcnow()
    one_hour = datetime.timedelta(hours=1)

    last_checked = config.get('last checked', now)

    # don't bother checking more than once an hour
    should_check = (now - last_checked) > one_hour
    if has_config and should_check:
        return

    update_check('cs251tk', version)

    config['last checked'] = last_checked

    with open('.cs251toolkitrc.yaml', 'w', encoding='utf-8') as config_file:
        contents = yaml.safe_dump(config, default_flow_style=False)
        config_file.write(contents)
