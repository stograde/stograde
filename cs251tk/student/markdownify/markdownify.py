import os
from collections import OrderedDict
from .process_file import process_file
from .find_warnings import find_warnings


def markdownify(spec_id, username, spec, basedir, debug):
    try:
        cwd = os.getcwd()
        results = {
            'spec': spec_id,
            'student': username,
            'warnings': {},
            'files': OrderedDict(),
        }

        inputs = spec.get('inputs', [])
        supporting = os.path.join(basedir, 'data', 'supporting')
        for filename in inputs:
            in_path = os.path.join(supporting, spec_id, filename)
            out_path = os.path.join(cwd, filename)
            with open(in_path, 'rb') as infile:
                contents = infile.read()
            with open(out_path, 'wb') as outfile:
                outfile.write(contents)

        for file in spec['files']:
            filename = file['filename']
            steps = file['commands']
            options = file['options']
            result = process_file(filename, steps, options, spec, cwd, supporting)
            results['files'][filename] = result

        try:
            for file in spec['files']:
                os.remove('{}.exec'.format(file['filename']))
            for inputfile in inputs:
                os.remove(inputfile)
        except FileNotFoundError:
            pass

        results['warnings'] = find_warnings()
        return results

    except Exception as err:
        if debug:
            raise err
        return {
            'spec': spec_id,
            'student': username,
            'warnings': {
                'Recording error': str(err),
            },
        }
