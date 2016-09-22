from os import path
from cs251tk.common import run


def clone(student, baseurl):
    if not path.exists(student):
        run(['git', 'clone', '--quiet', '{}/{}.git'.format(baseurl, student)])
