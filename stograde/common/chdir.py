import contextlib
import os


@contextlib.contextmanager
def chdir(path):
    """Create a `with` block for changing into a directory"""
    current_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(current_dir)
