from contextlib import contextmanager
import os


@contextmanager
def chdir(path):
    current_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(current_dir)
