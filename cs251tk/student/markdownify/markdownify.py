"""Given a spec, assuming we're in the homework folder, run the spec against the folder"""

import os
from collections import OrderedDict
from .process_file import process_file
from .find_warnings import find_warnings


def markdownify(spec_id, *, username, spec, basedir, debug, interact):
    """Run a spec against the current folder"""
    try:
        cwd = os.getcwd()
        results = {
            'spec': spec_id,
            'student': username,
            'warnings': find_warnings(),
            'files': OrderedDict(),
        }

        # prepare the current folder
        inputs = spec.get('inputs', [])
        supporting = os.path.join(basedir, 'data', 'supporting')
        # write the supporting files into the folder
        for filename in inputs:
            with open(os.path.join(supporting, spec_id, filename), 'rb') as infile:
                contents = infile.read()
            with open(os.path.join(cwd, filename), 'wb') as outfile:
                outfile.write(contents)

        for file in spec['files']:
            filename = file['filename']
            steps = file['commands']
            options = file['options']
            result = process_file(filename,
                                  steps=steps,
                                  options=options,
                                  spec=spec,
                                  cwd=cwd,
                                  supporting_dir=supporting,
                                  interact=interact)
            results['files'][filename] = result

        # now we remove any compiled binaries
        try:
            for file in spec['files']:
                os.remove('{}.exec'.format(file['filename']))
        except FileNotFoundError:
            pass

        # and we remove any supporting files
        try:
            for inputfile in inputs:
                os.remove(inputfile)
        except FileNotFoundError:
            pass

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
