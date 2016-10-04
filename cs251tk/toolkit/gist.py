import requests
import json
import getpass
__all__ = ['post_gist']


def get_auth():
    username = input('Github username: ')
    pw = getpass.getpass('Github password: ')
    return username, pw


def post_gist(description, files):
    username, password = get_auth()
    s = requests.Session()
    s.auth = (username, password)

    params = {
        'description': description,
        'files': files,
        'public': False,
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'User-Agent': 'stolaf-cs-toolkit/v1',
    }

    req = s.post('https://api.github.com/gists',
                 headers=headers,
                 data=json.dumps(params))

    result = req.json()

    return result.get('html_url', '"' + result.get('message', 'Error') + '"')
