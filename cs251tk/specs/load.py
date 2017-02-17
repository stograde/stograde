from logging import warning
from glob import iglob
import json

from .cache import cache_specs


def load_all_specs(basedir='.'):
    cache_specs(basedir)

    spec_files = iglob(basedir + '/data/specs/_cache/*.json')

    # load_spec returns a (name, spec) tuple, so we just let the dict() constructor
    # turn that into the {name: spec} pairs of a dictionary for us
    return dict([load_spec(filename) for filename in spec_files])


def load_some_specs(idents, basedir='.'):
    cache_specs(basedir)

    wanted_spec_files = [basedir + '/data/specs/_cache/{}.json'.format(ident) for ident in idents]
    all_spec_files = iglob(basedir + '/data/specs/_cache/*.json')
    loadable_spec_files = set(all_spec_files).intersection(wanted_spec_files)

    # load_spec returns a (name, spec) tuple, so we just let the dict() constructor
    # turn that into the {name: spec} pairs of a dictionary for us
    return dict([load_spec(filename) for filename in loadable_spec_files])


def load_spec(filename):
    with open(filename, 'r', encoding='utf-8') as specfile:
        loaded_spec = json.load(specfile)

    name = filename.split('/')[-1].split('.')[0]
    assignment = loaded_spec['assignment']

    if name != assignment:
        warning('assignment "{}" does not match the filename {}'.format(assignment, filename))

    return assignment, loaded_spec
