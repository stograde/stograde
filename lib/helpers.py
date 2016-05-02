'''Miscallaneous helper functions'''

from sys import stderr
from contextlib import contextmanager
from os.path import join, getsize
from os import walk, chdir as cd, getcwd
from itertools import groupby


@contextmanager
def chdir(path):
    '''Create a `with` block for changing into a directory'''
    current_dir = getcwd()
    try:
        cd(path)
        yield
    finally:
        cd(current_dir)


def warn(*args, **kwargs):
    '''Print a warning to stderr'''
    print(*args, file=stderr, **kwargs)


# from http://stackoverflow.com/a/2158532/2347774
def flatten(lst):
    '''Flatten a list'''
    for elem in lst:
        if isinstance(elem, list) and not isinstance(elem, str):
            yield from flatten(elem)
        else:
            yield elem


def size(path='.'):
    '''Get the size of a folder (including descendants)'''
    total_size = 0
    for dirpath, _, filenames in walk(path):
        for f in filenames:
            if not f.startswith('.'):
                try:
                    dir_size = getsize(join(dirpath, f))
                except OSError:
                    dir_size = 0
                total_size += dir_size
    return total_size


def add_newline_before(seq, lines):
    '''Adds a newline before each line in the input?'''
    new_lines = []
    for line in lines:
        if line and line[0:len(seq)] == seq:
            new_lines.append('\n' + line)
        else:
            new_lines.append(line)

    return ''.join(new_lines)


def pluck(lst, attr):
    '''Build a list of the values of the given attribute from the source list'''
    return [it[attr] for it in lst]


def group_by(iterable, predicate):
    sorted_iterable = sorted(iterable, key=predicate)
    grouped = groupby(sorted_iterable, key=predicate)
    for k, v in grouped:
        yield k, list(v)
