import requests
import natsort
import re
import pkg_resources  # part of setuptools
from .config import conf


def get_version(pkg):
    return pkg_resources.require(pkg)[0].version


def get_all_versions(pkg):
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


def update_available(pkg='cs251tk'):
    if not conf.needs_update_check():
        return None

    conf.set_last_update_check()

    current_version = get_version(pkg)
    all_versions = get_all_versions(pkg)

    if current_version not in all_versions:
        return current_version, None
    if all_versions.index(current_version) != len(all_versions) - 1:
        return current_version, all_versions[-1]

    return current_version, None
