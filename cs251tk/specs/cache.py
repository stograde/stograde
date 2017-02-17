from itertools import zip_longest
from logging import warning
from glob import iglob
import json
import copy
import os

import yaml


def cache_specs(basedir):
    """Convert YAML files to JSON to cache for future runs

    YAML parsing is incredibly slow, and JSON is quite fast,
    so we check modification times and convert any that have changed.
    """
    os.makedirs(basedir + '/data/specs/_cache', exist_ok=True)
    yaml_specs = iglob(basedir + '/data/specs/*.yaml')
    json_specs = iglob(basedir + '/data/specs/_cache/*.json')

    for yamlfile, jsonfile in zip_longest(yaml_specs, json_specs):
        if not yamlfile:
            # if yamlfile doesn't exist, then because we used zip_longest
            # there has to be a jsonfile. we don't want any jsonfiles
            # that don't match the yamlfiles.
            os.remove(jsonfile)
            continue

        if not jsonfile:
            jsonfile = yamlfile\
                .replace('specs/', 'specs/_cache/')\
                .replace('.yaml', '.json')

        y_modtime = get_modification_time_ns(yamlfile)
        j_modtime = get_modification_time_ns(jsonfile)
        if y_modtime != j_modtime:
            if not j_modtime:
                warning('caching', yamlfile, 'to', jsonfile)
                atime = os.stat(jsonfile).st_atime_ns
            else:
                atime = os.stat(yamlfile).st_atime_ns

            convert_spec(yamlfile, jsonfile)
            mtime = y_modtime
            os.utime(jsonfile, ns=(atime, mtime))


def convert_spec(yaml_path, json_path):
    with open(yaml_path, 'r', encoding='utf-8') as yamlfile:
        loaded = yaml.safe_load(yamlfile)

    edited = clarify_yaml(loaded)

    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(edited, jsonfile, default=json_date_handler)


def clarify_yaml(data):
    copied = copy.deepcopy(data)
    copied['files'] = [process_filelike_into_dict(f) for f in copied['files']]
    if 'tests' in copied:
        copied['tests'] = [process_filelike_into_dict(f) for f in copied['tests']]
    return copied


def process_filelike_into_dict(file_list):
    filename = file_list[0]
    commands = [f for f in file_list[1:] if isinstance(f, str)]
    option_list = [opt for opt in file_list[1:] if isinstance(opt, dict)]
    options = {k: v for opt in option_list for k, v in opt.items()}
    return {
        'filename': filename,
        'commands': commands,
        'options': options,
    }


def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError(
            'Object of type {} with value of {} is not JSON serializable'.format(
                type(obj),
                repr(obj)))


def get_modification_time_ns(path):
    try:
        return os.stat(path).st_mtime_ns
    except:
        return None


