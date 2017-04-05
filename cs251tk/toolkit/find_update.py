import requests
import natsort
import re
from cs251tk.common import version
from .config import conf


def get_all_versions(pkg='cs251tk'):
    # PyPI has these "simple" html pages. They're how pip does stuff.
    try:
        req = requests.get('https://pypi.python.org/simple/{}'.format(pkg), timeout=0.01)
    except requests.exceptions.ConnectionError:
        return []
    except requests.exceptions.Timeout:
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


def update_available(skip_update_check=False):
    if skip_update_check or not conf.needs_update_check():
        return version, None

    conf.set_last_update_check()

    all_versions = get_all_versions()

    if version not in all_versions:
        return version, None
    if all_versions.index(version) != len(all_versions) - 1:
        return version, all_versions[-1]

    return version, None
