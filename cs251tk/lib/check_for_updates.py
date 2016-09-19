'''Check for program updates'''
import datetime
from . import yaml
from .run import run
from .helpers import warn


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
    local_hash = config.get('local hash', None)
    remote_hash = config.get('remote hash', None)
    remote_is_local = config.get('remote hash exists locally', False)

    last_check_passed = local_hash == remote_hash
    # don't bother checking more than once an hour
    should_check = (now - last_checked) < one_hour
    if has_config and last_check_passed and should_check:
        return

    if not local_hash:
        _, local_hash = run(['git', 'rev-parse', 'master'])
        local_hash = local_hash.strip()

    if not remote_hash:
        _, remote_hash = run(['git', 'ls-remote', 'origin', 'master'])
        remote_hash = remote_hash.split()[0]

    if not remote_is_local:
        _, remote_is_local = run(['git', 'show', '--oneline', '--no-patch', remote_hash])
        remote_is_local = 'fatal' in remote_is_local

    if local_hash != remote_hash and not remote_is_local:
        warn('there is a toolkit update!')
        warn('a simple `git pull` should bring you up-to-date.')

    config['last checked'] = last_checked
    config['local hash'] = local_hash
    config['remote hash'] = remote_hash
    config['remote hash exists locally'] = remote_is_local

    with open('.cs251toolkitrc.yaml', 'w', encoding='utf-8') as config_file:
        contents = yaml.safe_dump(config, default_flow_style=False)
        config_file.write(contents)
