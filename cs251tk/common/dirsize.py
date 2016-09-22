import os


def dirsize(path='.'):
    """Get the size of a folder (including descendants)"""
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            if not f.startswith('.'):
                try:
                    dir_size = os.path.getsize(os.path.join(dirpath, f))
                except OSError:
                    dir_size = 0
                total_size += dir_size
    return total_size
