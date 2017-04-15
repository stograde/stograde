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
    os.makedirs(os.path.join(basedir, '_cache'), exist_ok=True)
    yaml_specs = iglob(os.path.join(basedir, '*.yaml'))
    json_specs = iglob(os.path.join(basedir, '_cache', '*.json'))

    for yamlfile, jsonfile in zip_longest(yaml_specs, json_specs):
        cache_spec(source_file=yamlfile, dest_file=jsonfile)


def cache_spec(*, source_file, dest_file):
    if not source_file:
        # If yamlfile doesn't exist, then because we used zip_longest
        # there has to be a jsonfile. We don't want any jsonfiles
        # that don't match the yamlfiles.
        os.remove(dest_file)
        return

    if not dest_file:
        dest_file = source_file \
            .replace('specs/', 'specs/_cache/') \
            .replace('.yaml', '.json')

    source_modtime = get_modification_time_ns(source_file)
    dest_modtime = get_modification_time_ns(dest_file)

    if source_modtime == dest_modtime:
        return

    if not dest_modtime:
        warning('caching {} to {}'.format(source_file, dest_file))
        atime = os.stat(source_file).st_atime_ns
    else:
        atime = os.stat(dest_file).st_atime_ns

    convert_spec(source_file, dest_file)
    mtime = source_modtime
    os.utime(dest_file, ns=(atime, mtime))


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
