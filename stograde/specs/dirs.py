import os


def get_specs_dir():
    return os.path.join(get_data_dir(), 'cs251tk', 'data')


def get_data_dir():
    return os.getenv('XDG_DATA_HOME', os.path.join(os.path.expanduser('~'), '.local', 'share'))
