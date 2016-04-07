from os.path import join, getsize
from os import walk


def size(path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in walk(path):
        for f in filenames:
            if not f.startswith('.'):
                fp = join(dirpath, f)
                try:
                    size = getsize(fp)
                except OSError:
                    size = 0
                total_size += size
    return total_size
