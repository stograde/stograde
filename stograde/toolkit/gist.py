"""Post a private gist of the analysis to github's gist service"""
import json
import getpass
import requests
__all__ = ['post_gist']


def get_auth():
    """Get the user's credentials"""
    username = input('Github username: ')
    password = getpass.getpass('Github password: ')
    return username, password


def post_gist(description, files):
    """Post a gist of the analysis"""
    username, password = get_auth()
    sess = requests.Session()
    sess.auth = (username, password)

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

    req = sess.post('https://api.github.com/gists',
                    headers=headers,
                    data=json.dumps(params))

    result = req.json()

    return result.get('html_url', '"' + result.get('message', 'Error') + '"')
