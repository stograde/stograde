import os


def create_students_dir(base_dir: str):
    os.makedirs(os.path.join(base_dir, 'students'), exist_ok=True)
