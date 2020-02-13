from logging import debug
import json
import copy
import os
from pathlib import Path

import yaml


def cache_specs(basedir):
    """Convert YAML files to JSON to cache for future runs

    YAML parsing is incredibly slow, and JSON is quite fast,
    so we check modification times and convert any that have changed.
    """

    basedir = Path(basedir)

    cachedir = basedir / '_cache'
    cachedir.mkdir(exist_ok=True, parents=True)

    known_json_specs = set()
    for specfile in basedir.glob('*.yaml'):
        dest = specfile.parent / '_cache' / f"{specfile.stem}.json"
        cache_spec(source_file=specfile, dest_file=dest)
        known_json_specs.add(dest)

    all_json_specs = set(cachedir.glob('*.json'))
    unknown_json_specs = all_json_specs - known_json_specs

    for cachedfile in unknown_json_specs:
        cachedfile.unlink()


def cache_spec(*, source_file, dest_file):
    if not source_file:
        # There should not be any jsonfiles without
        # corresponding yamlfiles
        os.remove(dest_file)
        return

    if not dest_file:
        dest_file = source_file \
            .replace('specs/', 'specs/_cache/') \
            .replace('.yaml', '.json')
        convert_spec(source_file, dest_file)
        return

    source_modtime = get_modification_time_ns(source_file)
    dest_modtime = get_modification_time_ns(dest_file)

    if source_modtime == dest_modtime:
        return

    if not dest_modtime:
        debug('caching {} to {}'.format(source_file, dest_file))
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
    if 'files' in copied and copied['files'] is not None:
        if copied.get('spec_version', 2) >= 3:
            copied['files'] = [process_file_yaml_into_dict(f) for f in copied['files']]
        else:
            copied['files'] = [process_file_yaml_into_dict_legacy(f) for f in copied['files']]
    if 'tests' in copied and copied['tests'] is not None:
        if copied.get('spec_version', 2) >= 3:
            copied['tests'] = [process_file_yaml_into_dict(f) for f in copied['tests']]
        else:
            copied['tests'] = [process_file_yaml_into_dict_legacy(f) for f in copied['tests']]
    return copied


def process_file_yaml_into_dict(file_list):
    filename = file_list['file']
    if filename is None:
        raise Exception("File name must be specified")

    commands = file_list.get('commands', [])
    if isinstance(commands, str):
        commands = [commands]
    assert isinstance(commands, list)

    options = file_list.get('options', {})
    assert isinstance(options, dict)

    return {
        'filename': filename,
        'commands': commands,
        'options': options,
    }


def process_file_yaml_into_dict_legacy(file_list):
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
    except Exception:
        return None
