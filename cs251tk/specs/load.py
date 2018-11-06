import sys
from logging import warning
from glob import iglob
import json
import os
import shutil

from ..common import chdir, run
from .cache import cache_specs
from .dirs import get_specs_dir


def load_all_specs(*, basedir=get_specs_dir(), skip_update_check=True):
    os.makedirs(basedir, exist_ok=True)

    if not skip_update_check:
        with chdir(basedir):
            res, _, _ = run(['git', 'fetch', 'origin'])

            if res != 'success':
                print("Error fetching specs", file=sys.stderr)

            _, res, _ = run(['git', 'log', 'HEAD..origin/master'])

        if res != '':
            pull = input('Spec updates found. Pull new specs? (Y/N)')
            if pull and pull.lower()[0] == "y":
                with chdir(basedir):
                    run(['git', 'pull', 'origin', 'master'])

    # the repo has a /specs folder
    basedir = os.path.join(basedir, 'specs')

    cache_specs(basedir)

    spec_files = iglob(os.path.join(basedir, '_cache', '*.json'))

    # load_spec returns a (name, spec) tuple, so we just let the dict() constructor
    # turn that into the {name: spec} pairs of a dictionary for us
    return dict([load_spec(filename, basedir) for filename in spec_files])


def load_some_specs(idents, *, basedir=get_specs_dir()):
    # the repo has a /specs folder
    basedir = os.path.join(basedir, 'specs')

    cache_specs(basedir)

    wanted_spec_files = [os.path.join(basedir, '_cache', '{}.json'.format(ident)) for ident in idents]
    all_spec_files = iglob(os.path.join(basedir, '_cache', '*.json'))
    loadable_spec_files = set(all_spec_files).intersection(wanted_spec_files)

    # load_spec returns a (name, spec) tuple, so we just let the dict() constructor
    # turn that into the {name: spec} pairs of a dictionary for us
    return dict([load_spec(filename) for filename in loadable_spec_files])


def load_spec(filename, basedir):
    with open(filename, 'r', encoding='utf-8') as specfile:
        loaded_spec = json.load(specfile)

    name = os.path.splitext(os.path.basename(filename))[0]
    assignment = loaded_spec['assignment']

    # Ask if user wants to re-cache specs to fix discrepancy
    if name != assignment:
        warning('assignment "{}" does not match the filename {}'.format(assignment, filename))
        recache = input("Re-cache specs? (Y/N)")
        if recache and recache.lower()[0] == "y":
            shutil.rmtree(os.path.join(basedir, '_cache'))
            cache_specs(basedir)

    return assignment, loaded_spec
