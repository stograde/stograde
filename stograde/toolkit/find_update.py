import natsort
import re
import requests

from .config import conf
from ..common import version


def get_all_versions(pkg='stograde'):
    # PyPI has these "simple" html pages. They're how pip does stuff.
    try:
        req = requests.get('https://pypi.python.org/simple/{}'.format(pkg), timeout=0.5)
    except requests.exceptions.ConnectionError:
        return []
    except requests.exceptions.Timeout:
        return []

    # Remove the first and last bits
    page = re.sub(r'.*</h1>|<br/>.*', '', req.text)
    # Grab just the links from the page
    lines = [line for line in page.splitlines() if line.strip().startswith('<a')]
    # Grab the file name and extract the version
    matches = [re.search(r">stograde-(?P<version>\d+\.\d+\.\d+)\.tar\.gz</a>", line) for line in lines]
    # Get the versions
    versions = [line.group("version") for line in matches if line]
    # Return the sorted list of all available versions
    return natsort.natsorted(set(versions))


def update_available():
    if not conf.needs_update_check():
        return version, None

    conf.set_last_update_check()

    all_versions = get_all_versions()

    if version not in all_versions:
        return version, None
    if all_versions.index(version) != len(all_versions) - 1:
        return version, all_versions[-1]

    return version, None
