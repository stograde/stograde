import requests
import json
import getpass
import yaml
from .config import load_config, save_config


def make_token():
    username = input('Github username: ')
    pw = getpass.getpass('Github password: ')

    client_id = '3a8d65b12aab30b654a6'
    client_secret = 'c8327b4008d460cbfac58cc82d3d6361c546e2fa'

    data = {'scopes': ['gist'], 'note': 'cs251-toolkit', 'client_secret': client_secret}
    req = requests.put('https://api.github.com/authorizations/clients/' + client_id,
                       auth=(username, pw),
                       data=json.dumps(data))

    result = req.json()
    return result['token']


def get_token():
    has_config, config = load_config()
    token = config.get('github token', None)

    if not token:
        token = make_token()
        config['github token'] = token
        save_config(config)

    return token


def post_gist(description, files):
    token = get_token()

    params = {
        'description': description,
        'files': files,
        'public': False,
    }

    headers = {
        'Authorization': 'token ' + token,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'User-Agent': 'stolaf-cs-toolkit/v1',
    }

    req = requests.post('https://api.github.com/gists',
                        headers=headers,
                        data=json.dumps(params))

    result = req.json()

    return result.get('html_url', '"' + result.get('message', 'Error') + '"')
