import shutil


def remove(student):
    try:
        shutil.rmtree(student)
    except FileNotFoundError:
        return
