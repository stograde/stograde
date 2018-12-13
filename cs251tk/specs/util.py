import os
from logging import warning


def get_filenames(spec):
    """returns the list of files from an assignment spec"""
    return [file['filename'] for file in spec['files']]


def check_dependencies(spec):
    for filepath in spec.get('dependencies', []):
        try:
            os.stat(filepath)
        except FileNotFoundError:
            warning('spec {}: required file "{}" could not be found'.format(spec['assignment'], filepath))
