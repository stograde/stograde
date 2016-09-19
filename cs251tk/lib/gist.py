import requests
import json
import getpass
import yaml


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
    with open('.cs251toolkitrc.yaml', 'r', encoding='utf-8') as infile:
        data = yaml.safe_load(infile.read())
        token = data.get('github token', None)
    if not token:
        token = make_token()
        data['github token'] = token
        with open('.cs251toolkitrc.yaml', 'w', encoding='utf-8') as file:
            file.write(yaml.safe_dump(data, default_flow_style=False))
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
