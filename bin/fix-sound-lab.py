#!/usr/bin/env python3

import os
import shutil

big = '''# OS-specific files
Thumbs.db
.DS_Store
.nfs*

# Compiled and object files
*.out
*.o

# Temporary files
*~
\#*\#

# Images
*.pbm
*.ppm
*.pam
*.jpg
*.jpeg
*.tiff
*.png
*.gif
*.webp

# Audio
*.wav
*.raw
*.mp3
*.aac
*.m4a

# Ignore doxygen output
*/html
*/latex
'''

lab2 = '''*.txt
'''


def ls():
    print(list(os.listdir('.')))


def rm(paths):
    for p in paths:
        shutil.rmtree(p)
        # os.remove(p)


def get_bin_files():
    return [f for f in os.listdir('.') if '.' not in f]


def get_temp_files():
    return [f for f in os.listdir('.') if f.endswith('~')]


def get_out_files():
    return [f for f in os.listdir('.') if f.split('.')[-1].startswith('out')]


def get_sounds_files():
    return [f for f in os.listdir('.') if f.endswith('wav') or f.endswith('mp3') or f.endswith('mp4') or f.endswith('txt')]


def get_doxygen():
    return [f for f in os.listdir('.') if f == 'html' or f == 'latex']


def clean():
    dirs = [d for d in ['hw8', 'hw9'] if os.path.isdir(d)]
    for folder in dirs:
        os.chdir(folder)

        files = []
        # files += get_bin_files()
        # files += get_out_files()
        # files += get_temp_files()
        # files += get_sounds_files()
        files += get_doxygen()
        # print(files)
        rm(set(files))

        os.chdir('..')


def gitignore():
    with open('.gitignore', 'w') as gitignore:
        gitignore.write(big)


for student in os.listdir('students'):
# for student in ['hoops']:
    student_dir = os.path.join('students', student)
    if os.path.isdir(student_dir):
        os.chdir(student_dir)
        try:
            print('cleaning up homeworks for {}'.format(student))
            clean()
            print('fixing gitignores for {}'.format(student))
            gitignore()
        finally:
            os.chdir(os.path.join('..', '..'))
