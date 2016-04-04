from sys import platform

win_frames = ['-', '\\', '|', '/']
ix_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

frames = win_frames if platform == 'win32' else ix_frames


def spinner():
    def inner():
        inner.i += 1
        return frames[inner.i % len(frames)]
    inner.i = 0

    return inner
