from os import remove as os_remove
from os import utime as os_utime
from os import stat as os_stat
from os import makedirs as makedirs
from itertools import zip_longest
from glob import iglob
import json
import copy
from .helpers import warn
from . import yaml


def load_specs():
    cache_specs()
    specs_idents = iglob('specs/_cache/*.json')
    specs = {}
    for filename in specs_idents:
        with open(filename, 'r', encoding='utf-8') as specfile:
            spec = specfile.read()
            if spec:
                loaded = json.loads(spec)
                name = filename.split('/')[2].split('.')[0]
                assignment = loaded['assignment']
                if name != assignment:
                    warn('assignment "{}" does not match the filename {}'.format(
                        assignment,
                        filename))
                specs[assignment] = loaded
            else:
                warn('Blank spec "{}"'.format(filename))
    return specs


def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError(
            'Object of type {} with value of {} is not JSON serializable'.format(
                type(obj),
                repr(obj)))


def process_file_into_dict(file_list):
    filename = file_list[0]
    commands = [f for f in file_list[1:] if type(f) is str]
    option_list = [opt for opt in file_list[1:] if type(opt) is dict]
    options = { k: v for opt in option_list for k, v in opt.items() }
    return {
        'filename': filename,
        'commands': commands,
        'options': options,
    }


def clarify_yaml(data):
    copied = copy.deepcopy(data)
    copied['files'] = [process_file_into_dict(f) for f in copied['files']]
    if 'tests' in copied:
        copied['tests'] = [process_file_into_dict(f) for f in copied['tests']]
    return copied


def convert_spec(yaml_path, json_path):
    with open(yaml_path, 'r', encoding='utf-8') as yamlfile:
        data = yamlfile.read()

    loaded = yaml.safe_load(data)
    edited = clarify_yaml(loaded)
    stringified = json.dumps(edited, default=json_date_handler)

    with open(json_path, 'w', encoding='utf-8') as jsonfile:
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
    makedirs('specs/_cache', exist_ok=True)
    yaml_specs = iglob('specs/*.yaml')
    json_specs = iglob('specs/_cache/*.json')
    for yamlfile, jsonfile in zip_longest(yaml_specs, json_specs):
        if not yamlfile:
            # if yamlfile doesn't exist, then because we used zip_longest
            # there has to be a jsonfile. we don't want any jsonfiles
            # that don't match the yamlfiles.
            os_remove(jsonfile)
            continue

        if not jsonfile:
            jsonfile = yamlfile.replace('specs/', 'specs/_cache/').replace('.yaml', '.json')

        y_modtime = get_modification_time_ns(yamlfile)
        j_modtime = get_modification_time_ns(jsonfile)
        if y_modtime != j_modtime:
            if j_modtime is not None:
                warn('caching', yamlfile, 'to', jsonfile)
                atime = os_stat(jsonfile).st_atime_ns
            else:
                atime = os_stat(yamlfile).st_atime_ns

            convert_spec(yamlfile, jsonfile)
            mtime = y_modtime
            os_utime(jsonfile, ns=(atime, mtime))


def get_filenames(spec):
    '''returns the list of files from an assignment spec'''
    return [file['filename'] for file in spec['files']]
