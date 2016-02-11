#!/usr/bin/env python3

import os
from argparse import ArgumentParser
from lib.columnize import columnize
from lib.run_command import run
from lib.markdownify import markdownify
from lib.progress import progress
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


def message(user):
    return lambda m: '%s [%s]' % (user, m)


def main(record=[], students=[],
         day='', date='',
         no_update=False, clean=False, output=None,
         quiet=False, sort_by='name'):
    table = ''
    root = os.getcwd()

    if day:
        day = run(['date', '-v1w', '-v-' + day, '+%Y-%m-%d'])
        print('Checking out %s at 5:00pm' % day)
    elif date:
        print('Checking out %s at 5:00pm' % date)

    ext = 'md'
    if output:
        ext = output

    recordings = {}
    if record:
        filenames = {}
        specs = {}
        for to_record in record:
            filenames[to_record] = './logs/log-' + to_record
            recordings[to_record] = open(filenames[to_record] + '.md', 'w')
            specs[to_record] = open(root + '/specs/' + to_record + '.yaml', 'r').read()
            if specs[to_record]:
                specs[to_record] = yaml.load(specs[to_record])

    os.makedirs('./students', exist_ok=True)
    os.chdir('./students')

    for i, user in enumerate(students):
        i = i + 1
        progress(len(students), i, message=user)

        msg = message(user)

        if clean:
            progress(len(students), i, message=msg('cleaning'))
            shutil.rmtree(user)

        if not os.path.exists(user):
            progress(len(students), i, message=msg('cloning'))
            git_clone = 'git clone --quiet %s/%s.git' % (stogit, user)
            run(git_clone.split())

        os.chdir(user)

        progress(len(students), i, message=msg('stashing'))
        if run('git status --porcelain'.split())[1]:
            run('git stash -u'.split())
            run('git stash clear'.split())

        if not no_update:
            progress(len(students), i, message=msg('updating'))
            run('git pull --quiet origin master'.split())

        if day or date:
            progress(len(students), i, message=msg('checkouting'))
            git_checkout = 'git checkout (git rev-list -n 1 --before="%s 18:00" master) --force --quiet' % (day)
            run(git_checkout.split())

        all_folders = [folder
                       for folder in os.listdir('.')
                       if not folder.startswith('.') and os.path.isdir(folder)]

        filtered = [folder for folder in all_folders if size(folder) > 100]
        FOLDERS = sorted([folder.lower() for folder in filtered])
        HWS = {foldername: foldername.startswith('hw') for foldername in FOLDERS}
        LABS = {foldername: foldername.startswith('lab') for foldername in FOLDERS}

        if record:
            for to_record in record:
                if os.path.exists(to_record):
                    progress(len(students), i, message=msg('recording %s' % to_record))
                    os.chdir(to_record)
                    recording = markdownify(to_record, user, specs[to_record])
                    recordings[to_record].write(recording)
                    os.chdir('..')

        table += "%s\t%s\t%s\n" % (user,
                                   ' '.join([h for h, result in HWS.items() if result]),
                                   ' '.join([l for l, result in LABS.items() if result]))

        if day:
            run('git checkout master --quiet --force'.split())

        os.chdir('..')

    [recording.close() for name, recording in recordings.items()]

    os.chdir('..')

    return '\n' + columnize(table.splitlines(), sort_by=sort_by)


if __name__ == '__main__':
    parser = ArgumentParser(description='The core of the CS251 toolkit.')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Be quieter')
    parser.add_argument('--no-update', '-n', action='store_true',
                        help='Do not update the student folders before checking.')
    parser.add_argument('--day', action='store',
                        help='Check out the state of the student folder as of 5pm on the last <day> (mon, wed, fri, etc).')
    parser.add_argument('--date', action='store',
                        help='Check out the state of the student folder as of 5pm on <date> (Y-M-D).')
    parser.add_argument('--clean', action='store_true',
                        help='Remove student folders and re-clone them')
    parser.add_argument('--record', action='append', nargs='+', metavar='HW',
                        help='Record information on the student\'s submissions. Must be folder name to record.')
    # parser.add_argument('--output', action='store', nargs='?', default=None,
    #                     help='The type of log file that pandoc should generate.')
    parser.add_argument('--students', action='append', nargs='+', metavar='STUDENT',
                        help='Only iterate over these students.')
    parser.add_argument('--sort-by', action='store', default='name', type=str, choices=['name', 'homework'],
                        help='Sort by either student name or homework count.')
    args = vars(parser.parse_args())

    # argparser puts it into a nested list because you could have two
    # occurrences of the arg, each with a variable number of arguments
    # like `--students amy max --students rives` would become `[[amy, max], [rives]]`
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

    output = main(**args)
    if not args['quiet']:
        print(output)
