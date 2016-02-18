#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser
from lib.columnize import columnize
from lib.run_command import run
from lib.markdownify import markdownify
from lib.progress import progress as progress_bar
from lib.flatten import flatten
import lib.yaml as yaml
import shutil

stogit = 'git@stogit.cs.stolaf.edu:sd-s16'


def size(path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if not f.startswith('.'):
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
    return total_size


def get_args():
    parser = ArgumentParser(description='The core of the CS251 toolkit.')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Be quieter')
    parser.add_argument('--no-update', '-n', action='store_true',
                        help='Do not update the student folders before checking.')
    parser.add_argument('--day', action='store',
                        help='Check out the student folder as of 5pm on the last <day of week>.')
    parser.add_argument('--date', action='store',
                        help='Check out the student folder as of 5pm on <date> (Y-M-D).')
    parser.add_argument('--clean', action='store_true',
                        help='Remove student folders and re-clone them')
    parser.add_argument('--record', action='append', nargs='+', metavar='HW',
                        help="Record information on student submissions. Requires a spec file.")
    parser.add_argument('--students', action='append', nargs='+', metavar='STUDENT',
                        help='Only iterate over these students.')
    parser.add_argument('--sort-by', action='store', default='name', type=str,
                        choices=['name', 'homework'],
                        help='Sort by either student name or homework count.')
    return vars(parser.parse_args())


def single_student(student, index, args={}, specs={}, recordings={}):
    def progress(message):
        return progress_bar(len(args['students']), index, message='%s [%s]' % (student, message))

    if args['clean']:
        progress('cleaning')
        shutil.rmtree(student)

    if not os.path.exists(student):
        progress('cloning')
        git_clone = 'git clone --quiet %s/%s.git' % (stogit, student)
        run(git_clone.split())

    os.chdir(student)

    retval = ''

    try:
        progress('stashing')
        if run('git status --porcelain'.split())[1]:
            run('git stash -u'.split())
            run('git stash clear'.split())

        if not args['no_update']:
            progress('updating')
            run('git pull --quiet origin master'.split())

        if args['day']:
            progress('checkouting')
            git_checkout = 'git checkout (git rev-list -n 1 --before="%s 18:00" master) --force --quiet' % (day)
            run(git_checkout.split())

        all_folders = [folder
                       for folder in os.listdir('.')
                       if not folder.startswith('.') and os.path.isdir(folder)]

        filtered = [f for f in all_folders if size(f) > 100]
        FOLDERS = sorted([f.lower() for f in filtered])
        HWS = {f: f.startswith('hw') for f in FOLDERS}
        LABS = {f: f.startswith('lab') for f in FOLDERS}

        if args['record']:
            for to_record in args['record']:
                if os.path.exists(to_record):
                    progress('recording %s' % to_record)
                    os.chdir(to_record)
                    try:
                        recording = markdownify(to_record, student, specs[to_record])
                        recordings[to_record].write(recording)
                    finally:
                        os.chdir('..')

        retval = "%s\t%s\t%s\n" % (student,
                                   ' '.join([h for h, result in HWS.items() if result]),
                                   ' '.join([l for l, result in LABS.items() if result]))

        if args['day']:
            run('git checkout master --quiet --force'.split())

    finally:
        os.chdir('..')

    return retval


def main():
    args = get_args()

    # argparser puts it into a nested list because you could have two
    # occurrences of the arg, each with a variable number of arguments.
    # `--students amy max --students rives` => `[[amy, max], [rives]]`
    args['students'] = list(flatten(args['students'] or []))
    args['record'] = list(flatten(args['record'] or []))

    if not args['students']:
        if os.path.exists('./students.txt'):
            with open('./students.txt') as infile:
                args['students'] = infile.read().splitlines()
        else:
            print('Either provide a --student argument, a ./students.txt file, or a list of usernames to stdin, please.', file=sys.stderr)
            sys.exit(1)

    elif '-' in args['students']:
        args['students'] = flatten(args['students'] + sys.stdin.read().splitlines())
        args['students'] = [student for student in args['students'] if student != '-']

    elif '-' in args['record']:
        args['record'] = flatten(args['record'] + sys.stdin.read().splitlines())
        args['record'] = [to_record for to_record in args['record'] if to_record != '-']

    table = ''
    root = os.getcwd()

    if args['day']:
        args['day'] = run(['date', '-v1w', '-v-' + day, '+%Y-%m-%d'])
        print('Checking out %s at 5:00pm' % day)
    elif args['date']:
        args['day'] = args['date']
        print('Checking out %s at 5:00pm' % date)

    recordings = {}
    filenames = {}
    specs = {}
    if args['record']:
        for to_record in args['record']:
            filenames[to_record] = './logs/log-' + to_record
            recordings[to_record] = open(filenames[to_record] + '.md', 'w')
            specs[to_record] = open(root + '/specs/' + to_record + '.yaml', 'r').read()
            if specs[to_record]:
                specs[to_record] = yaml.load(specs[to_record])

    os.makedirs('./students', exist_ok=True)
    os.chdir('./students')

    try:
        for i, student in enumerate(args['students']):
            table += single_student(student, i + 1,
                                    args=args, specs=specs,
                                    recordings=recordings)

    finally:
        [recording.close() for name, recording in recordings.items()]

        os.chdir('..')

    if not args['quiet']:
        print('\n' + columnize(table.splitlines(), sort_by=args['sort_by']))


if __name__ == '__main__':
    main()
