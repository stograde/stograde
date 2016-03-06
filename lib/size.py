import os


def size(path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if not f.startswith('.'):
                fp = os.path.join(dirpath, f)
                try:
                    size = os.path.getsize(fp)
                except OSError:
                    size = 0
                total_size += size
    return total_size
