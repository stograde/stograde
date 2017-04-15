import os


def get_specs_dir():
    return os.path.join(get_data_dir(), 'cs251tk', 'specs')


def get_data_dir():
    return os.getenv('XDG_DATA_HOME', os.path.join(os.getenv('HOME'), '.local', 'share'))
