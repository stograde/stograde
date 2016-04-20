from os import remove as os_remove
from os import utime as os_utime
from os import stat as os_stat
from itertools import zip_longest
from glob import iglob
from .warn import warn
from . import size
from . import yaml
import json


def load_specs():
    cache_specs()
    specs_idents = iglob('specs/*.json')
    specs = {}
    for s in specs_idents:
        with open(s, 'r', encoding='utf-8') as specfile:
            spec = specfile.read()
            if spec:
                loaded = json.loads(spec)
                name = s.split('/')[1].split('.')[0]
                assignment = loaded['assignment']
                if name != assignment:
                    warn('the assignment "{}" does not match the filename {}'.format(assignment, s))
                specs[assignment] = loaded
            else:
                warn('Blank spec "{}"'.format(s))
    return specs


def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, ...):
        return ...
    else:
        raise TypeError(
            'Object of type {} with value of {} is not JSON serializable'.format(
                type(obj),
                repr(obj)))


def convert_spec(yaml_path, json_path):
    with open(yaml_path, 'r', encoding='utf-8') as yamlfile:
        with open(json_path, 'w', encoding='utf-8') as jsonfile:
            data = yamlfile.read()
            loaded = yaml.safe_load(data)
            stringified = json.dumps(loaded, default=json_date_handler)
            jsonfile.write(stringified)


def get_modification_time_ns(path):
    try:
        return os_stat(path).st_mtime_ns
    except:
        return None


def cache_specs():
    # Convert YAML files to JSON to cache for future runs
    # YAML parsing is incredibly slow, and JSON is quite fast,
    # so we check modification times and convert any that have changed.
    yaml_specs = iglob('specs/*.yaml')
    json_specs = iglob('specs/*.json')
    for yamlfile, jsonfile in zip_longest(yaml_specs, json_specs):
        if not yamlfile:
            # if yamlfile doesn't exist, then because we used zip_longest
            # there has to be a jsonfile. we don't want any jsonfiles
            # that don't match the yamlfiles.
            os_remove(jsonfile)
            continue

        if not jsonfile:
            jsonfile = yamlfile.replace('.yaml', '.json')

        y_modtime = get_modification_time_ns(yamlfile)
        j_modtime = get_modification_time_ns(jsonfile)
        if y_modtime != j_modtime:
            if j_modtime is not None:
                warn('diff. times!', 'yaml', y_modtime, 'json', j_modtime)
                atime = os_stat(jsonfile).st_atime_ns
            else:
                atime = os_stat(yamlfile).st_atime_ns

            convert_spec(yamlfile, jsonfile)
            mtime = y_modtime
            os_utime(jsonfile, ns=(atime, mtime))


def get_files(spec):
    '''returns the list of files from an assignment spec'''
    return [filename
            for file in spec['files']
            for filename in file]


def get_files_and_steps(spec):
    '''returns the list of files from an assignment spec'''
    return [(filename, steps)
            for file in spec['files']
            for filename, steps in file.items()]
