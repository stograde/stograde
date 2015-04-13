#!/usr/bin/env python3

from argparse import ArgumentParser
from _scripts.columnize import main as columnize
from _scripts.run_command import run
from _scripts.markdownify import markdownify
from _scripts.progress import progress
from _scripts.flatten import flatten
import shutil
import os
import sys

stogit = 'git@stogit.cs.stolaf.edu:sd-s15'


def size(path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            if not f.startswith('.'):
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
    return total_size


def main(no_update=False, day='', clean=False, record=[], students=[], output=None):
    table = ''

    if day:
        day = run(['date', '-v1w', '-v-' + day, '+%Y-%m-%d'])
        print('Checking out %s at 5:00pm' % day)

    ext = 'md'
    if output:
        ext = output

    if record:
        filenames = {}
        recordings = {}
        for to_record in record:
            filenames[to_record] = './_logs/log-' + to_record
            recordings[to_record] = open(filenames[to_record] + '.md', 'w')

    os.chdir('./_users')

    for i, user in enumerate(students):
        progress(len(students), i+1, message=user)

        if clean:
            progress(len(students), i+1, message=user + ' [cleaning]')
            shutil.rmtree(user)

        if not os.path.exists(user):
            progress(len(students), i+1, message=user + ' [cloning]')
            git_clone = 'git clone --quiet %s/%s.git' % (stogit, user)
            run(git_clone.split())

        os.chdir(user)

        progress(len(students), i+1, message=user + ' [stashing]')
        run('git stash -u'.split())
        run('git stash clear'.split())

        if not no_update:
            progress(len(students), i+1, message=user + ' [updating]')
            run('git pull --rebase --quiet origin master'.split())

        if day:
            progress(len(students), i+1, message=user + ' [checkouting]')
            git_checkout = 'git checkout (git rev-list -n 1 --before="%s 18:00" master) --force --quiet' % (day)
            run(git_checkout.split())

        if record:
            for to_record in record:
                if os.path.exists(to_record):
                    progress(len(students), i+1, message=user + ' [recording %s]' % to_record)
                    os.chdir(to_record)
                    recordings[to_record].write(markdownify(to_record, user))
                    os.chdir('..')

        all_folders = [folder for folder in os.listdir('.') if (not folder.startswith('.') and os.path.isdir(folder))]

        filtered = [folder for folder in all_folders if size(folder) > 100]
        FOLDERS = sorted([folder.lower() for folder in filtered])
        HWS = [foldername for foldername in FOLDERS if 'hw' in foldername]
        LABS = [foldername for foldername in FOLDERS if 'hw' not in foldername]

        table += "%s\t%s\t%s\n" % (user, ' '.join(HWS), ' '.join(LABS))

        if day:
            run('git checkout master --quiet --force'.split())

        os.chdir('..')

    os.chdir('..')

    # if record and output:
    #     os.chdir('_logs')
    #     for filename in filenames:
    #         run(['pandoc', '--standalone', '--from=markdown_github', '--to='+output, '--output=%s.%s' % (filename, output), filename + '.md'])
    #     os.chdir('..')

    return '\n' + columnize(table.splitlines())


if __name__ == '__main__':
    parser = ArgumentParser(description='The core of the CS251 toolkit.')
    parser.add_argument('--no-update', action='store_true', help='Do not update the student folders before checking.')
    parser.add_argument('--day', action='store', help='Check out the state of the student folder as of 5pm on the last <day> (mon, wed, fri, etc).')
    parser.add_argument('--clean', action='store_true', help='Remove student folders and re-clone them')
    parser.add_argument('--record', action='append', nargs='+', metavar='HW', help='Record information on the student\'s submissions. Must be folder name to record.')
    # parser.add_argument('--output', action='store', nargs='?', default=None, help='The type of log file that pandoc should generate.')
    parser.add_argument('--students', action='append', nargs='+', metavar='STUDENT', help='Only iterate over these students.')
    args = vars(parser.parse_args())

    # argparser puts it into a nested list because you could have two occurrences of the arg, each with a variable number of arguments
    # like --students amy max --students rives would become [[amy, max], [rives]]
    args['students'] = list(flatten(args['students'] or []))
    args['record'] = list(flatten(args['record'] or []))

    if not args['students']:
        if os.path.exists('./students.txt'):
            with open('./students.txt') as infile:
                args['students'] = infile.read().splitlines()

        else:
            print('Either provide a --student argument, a ./students.txt file, or usernames to stdin, please.', file=sys.stderr)
            sys.exit(1)

    elif '-' in args['students']:
        args['students'] = flatten(args['students'] + sys.stdin.read().splitlines())
        args['students'] = [student for student in args['students'] if student != '-']

    elif '-' in args['record']:
        args['record'] = flatten(args['record'] + sys.stdin.read().splitlines())
        args['record'] = [to_record for to_record in args['record'] if to_record != '-']

    print(main(**args))
