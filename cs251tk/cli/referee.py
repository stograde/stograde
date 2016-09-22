import sys
from os import makedirs, getcwd

from cs251tk.common import chdir
from cs251tk.referee import process_student
from cs251tk.referee import process_args
from cs251tk.specs import load_specs


def main():
    args = process_args()
    basedir = getcwd()

    specs = load_specs()
    if not specs:
        print('no specs loaded!')
        sys.exit(1)

    commits = args['HASH']
    student = args['USERNAME']
    stogit = args['STOGIT_URL']

    for ref in commits:
        result, recording = process_student(student, ref=ref, stogit=student, specs=specs, basedir=basedir)
        results.append(result)
        records.append(recording)

    # send_recordings(records, args['students'])
