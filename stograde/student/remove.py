import shutil


def remove(student: str):
    try:
        shutil.rmtree(student)
    except FileNotFoundError:
        return
