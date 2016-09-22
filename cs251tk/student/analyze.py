import re
import os

from cs251tk.common import chdir
from cs251tk.common import find_unmerged_branches_in_cwd
from cs251tk.specs import get_filenames


def analyze(student, specs, check_for_branches):
    unmerged_branches = has_unmerged_branches(student, check_for_branches)

    results = {}
    with chdir(student):
        for spec in specs.values():
            assignment = spec['assignment']
            results[assignment] = analyze_assignment(spec, assignment)

    homework_list = [result for result in results.values() if result['kind'] == 'homework']
    lab_list = [result for result in results.values() if result['kind'] == 'lab']

    return {
        'username': student,
        'unmerged_branches': unmerged_branches,
        'homeworks': homework_list,
        'labs': lab_list,
    }


def analyze_assignment(spec, assignment):
    folder = spec.get('folder', assignment)
    kind, num = parse_assignment_name(assignment)
    results = {'number': num, 'kind': kind}

    if not os.path.exists(folder):
        results['status'] = 'missing'
        return results

    with chdir(folder):
        files_that_do_exist = set(os.listdir('.'))
        files_which_should_exist = set(get_filenames(spec))
        intersection_of = files_that_do_exist.intersection(files_which_should_exist)

        if intersection_of == files_which_should_exist:
            # if every file that should exist, does: we're good.
            results['status'] = 'success'
        elif intersection_of:
            # if some files that should exist, do: it's a partial assignment
            results['status'] = 'partial'
        else:
            # otherwise, none of the required files are there
            results['status'] = 'missing'

    return results


def parse_assignment_name(name):
    """returns the kind and number from an assignment name"""
    matches = re.match(r'([a-zA-Z]+)(\d+)', name).groups()
    kind = matches[0]
    if kind == 'hw':
        kind = 'homework'
    elif kind == 'lab':
        kind = 'lab'
    num = int(matches[1])
    return kind, num


def has_unmerged_branches(student, should_check):
    with chdir(student):
        if should_check:
            return find_unmerged_branches_in_cwd()
        return None
