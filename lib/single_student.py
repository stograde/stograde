from os import path, listdir
import shutil
import re
from .find_unmerged_branches_in_cwd import find_unmerged_branches_in_cwd
from .markdownify import markdownify
from .specs import get_filenames
from .helpers import chdir
from .run import run

STOGIT = 'git@stogit.cs.stolaf.edu:sd-s16'


def remove(student):
    shutil.rmtree(student)


def clone(student):
    if not path.exists(student):
        run(['git', 'clone', '--quiet', '{}/{}.git'.format(STOGIT, student)])


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
    recordings = []
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

            recordings.append(recording)

    return recordings


def parse_assignment_name(name):
    '''returns the kind and number from an assignment name'''
    matches = re.match(r'([a-zA-Z]+)(\d+)', name).groups()
    kind = matches[0]
    if kind == 'hw':
        kind = 'homework'
    elif kind == 'lab':
        kind = 'lab'
    num = int(matches[1])
    return kind, num


def analyze(student, specs, args):
    unmerged_branches = has_unmerged_branches(student, args)

    results = {}
    with chdir(student):
        for spec in specs.values():
            assignment = spec['assignment']
            folder = spec.get('folder', assignment)
            kind, num = parse_assignment_name(assignment)
            results[assignment] = {'number': num, 'kind': kind}

            if not path.exists(folder):
                results[assignment]['status'] = 'missing'
                continue

            with chdir(folder):
                files_that_do_exist = set(listdir())
                files_which_should_exist = set(get_filenames(spec))
                intersection_of = files_that_do_exist.intersection(files_which_should_exist)

                if intersection_of == files_which_should_exist:
                    # if every file that should exist, does: we're good.
                    results[assignment]['status'] = 'success'
                elif intersection_of:
                    # if some files that should exist, do: it's a partial assignment
                    results[assignment]['status'] = 'partial'
                else:
                    # otherwise, none of the required files are there
                    results[assignment]['status'] = 'missing'

    homework_list = [result for result in results.values() if result['kind'] == 'homework']
    lab_list = [result for result in results.values() if result['kind'] == 'lab']

    return {
        'username': student,
        'unmerged_branches': unmerged_branches,
        'homeworks': homework_list,
        'labs': lab_list,
    }


def reset(student, args):
    with chdir(student):
        if args['day']:
            run(['git', 'checkout', 'master', '--quiet', '--force'])


def single_student(student, args={}, specs={}):
    recordings = []
    retval = {}

    if args['clean']:
        remove(student)

    clone(student)

    try:
        stash(student, args)
        pull(student, args)

        checkout_day(student, args)

        recordings = record(student, specs, args)
        retval = analyze(student, specs, args)

        reset(student, args)

    except Exception as err:
        retval = {'username': student, 'error': err}

    return retval, recordings
