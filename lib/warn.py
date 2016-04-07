from sys import stderr


def warn(*args, **kwargs):
    print(*args, file=stderr, **kwargs)
