from os import path, listdir
import shutil
from .find_unmerged_branches_in_cwd import find_unmerged_branches_in_cwd
from .markdownify import markdownify
from .flatten import flatten
from .chdir import chdir
from .size import size
from .warn import warn
from .run import run

stogit = 'git@stogit.cs.stolaf.edu:sd-s16'
labnames = {
    'sound': ['lab2', 'lab3'],
    'images': ['lab4', 'lab5', 'lab6'],
}


def remove(student):
    shutil.rmtree(student)


def clone(student):
    if not path.exists(student):
        run(['git', 'clone', '--quiet', '{}/{}.git'.format(stogit, student)])


def has_changed_files():
    _, output = run(['git', 'status', '--porcelain'])
    return bool(output)


def stash(student, args):
    with chdir(student):
        if not args['no_update'] and has_changed_files():
            run(['git', 'stash', '-u'])
            run(['git', 'stash', 'clear'])


def pull(student, args):
    with chdir(student):
        if not args['no_update']:
            run(['git', 'pull', '--quiet', 'origin', 'master'])


def checkout_day(student, args):
    with chdir(student):
        if args['day']:
            rev_list = ['git', 'rev-list', '-n', '1', '--before="{} 18:00"'.format(day), 'master']
            _, rev = run(rev_list)
            run(['git', 'checkout', rev, '--force', '--quiet'])


def has_unmerged_branches(student, args):
    with chdir(student):
        if args['no_check']:
            return None
        else:
            return find_unmerged_branches_in_cwd()


def record(student, specs, args):
    recordings = {}
    if not args['record']:
        return recordings

    with chdir(student):
        for to_record in args['record']:
            if path.exists(to_record):
                with chdir(to_record):
                    recording = markdownify(to_record, student, specs[to_record])
            else:
                recording = {
                    'spec': to_record,
                    'student': student,
                    'warnings': {'no submission': True},
                }

            recordings[to_record] = recording

    return recordings


def build_table_row(student, unmerged_branches):
    with chdir(student):
        all_folders = [folder
                       for folder in listdir('.')
                       if not folder.startswith('.') and path.isdir(folder)]
        filtered = [f for f in all_folders if size(f) > 100]

    FOLDERS = sorted([f.lower() for f in filtered])
    FOLDERS = list(flatten([(labnames[f] if f in labnames else f) for f in FOLDERS]))
    HWS = [f for f in FOLDERS if f.startswith('hw')]
    LABS = [f for f in FOLDERS if f.startswith('lab')]

    student_name = student + ' !' if unmerged_branches else student
    homework_list = ' '.join(HWS)
    lab_list = ' '.join(LABS)

    return "{}\t{}\t{}".format(student_name, homework_list, lab_list)


def reset(student, args):
    with chdir(student):
        if args['day']:
            run(['git', 'checkout', 'master', '--quiet', '--force'])


def single_student(student, args={}, specs={}):
    recordings = {}
    retval = ''

    if args['clean']:
        remove(student)

    clone(student)

    try:
        stash(student, args)
        pull(student, args)

        checkout_day(student, args)

        recordings = record(student, specs, args)

        unmerged_branches = has_unmerged_branches(student, args)
        retval = build_table_row(student, unmerged_branches)

        reset(student, args)

    except Exception as err:
        retval = "{}: {}".format(student, err)

    return student, retval, recordings
