import sys
from os import makedirs, getcwd

from cs251tk.common import chdir
from cs251tk.student import single_student
from cs251tk.toolkit import process_args
from .specs import load_specs


def main():
    args = process_args()
    basedir = getcwd()

    if args['day']:
        print('Checking out {} at 5:00pm'.format(args['day']))

    specs = load_specs()
    if not specs:
        print('no specs loaded!')
        sys.exit(1)

    results = []
    records = []
    makedirs('./students', exist_ok=True)
    with chdir('./students'):
        for student in args['students']:
            result, recording = single_student(student, args=args, specs=specs, basedir=basedir)
            results.append(result)
            records.append(recording)

    send_recordings(records, args['students'])
