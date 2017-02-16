import requests
import natsort
import re
from cs251tk.common import version
from .config import conf


def get_all_versions(pkg='cs251tk'):
    # PyPI has these "simple" html pages. They're how pip does stuff.
    try:
        req = requests.get('https://pypi.python.org/simple/{}'.format(pkg))
    except requests.exceptions.ConnectionError:
        return []

    # Remove the first and last bits
    page = re.sub(r'.*</h1>|<br/>.*', '', req.text)
    # Grab just the links from the page
    lines = [l for l in page.splitlines() if l.startswith('<a')]
    # Grab just the middles of the links
    packages = [re.sub('.*>(.*)<.*', '\\1', l) for l in lines]
    # Remove the suffixes
    versions = [re.sub(r'(\d)-.*|\.tar.gz', '\\1', l) for l in packages]
    # Remove the prefixes
    versions = [re.sub(r'.*-(\d)', '\\1', l) for l in versions]
    # Return the sorted list of all available versions
    return natsort.natsorted(set(versions))


def update_available():
    if not conf.needs_update_check():
        return current_version, None

    conf.set_last_update_check()

    current_version = version
    all_versions = get_all_versions()

    if current_version not in all_versions:
        return current_version, None
    if all_versions.index(current_version) != len(all_versions) - 1:
        return current_version, all_versions[-1]

    return current_version, None
