"""Post a private gist of the analysis to github's gist service"""
import getpass
import json
import requests
from typing import Tuple, Dict

__all__ = ['post_gist']


def get_auth() -> Tuple[str, str]:
    """Get the user's credentials"""
    username = input('Github username: ')
    token = getpass.getpass('Github personal access token: ')
    return username, token


def post_gist(description: str, files: Dict[str, Dict[str, str]]) -> str:
    """Post a gist of the analysis"""
    username, token = get_auth()
    sess = requests.Session()

    params = {
        'description': description,
        'files': files,
        'public': False,
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token {}'.format(token),
        'Content-Type': 'application/json',
        'User-Agent': 'stolaf-cs-toolkit/v1',
        'X-Github-Username': username,
    }

    req = sess.post('https://api.github.com/gists',
                    headers=headers,
                    data=json.dumps(params))

    result = req.json()

    return result.get('html_url', '"' + result.get('message', 'Error') + '"')
