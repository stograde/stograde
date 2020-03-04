import os


def import_supporting(*, spec, spec_id, basedir):
    cwd = os.getcwd()
    supporting_files = spec.get('inputs', []) + spec.get('supporting', [])
    supporting_dir = os.path.join(basedir, 'data', 'supporting')
    written_files = []

    # write the supporting files into the folder
    for filename in supporting_files:
        if isinstance(filename, list):
            if len(filename) == 1:
                in_name = filename[0]
                out_name = filename[0]
            else:
                in_name = filename[0]
                out_name = filename[1]
        elif isinstance(filename, dict):
            in_name = filename['file']
            out_name = filename.get('destination', filename.get('dest', in_name))
        elif isinstance(filename, str):
            in_name = filename
            out_name = filename
        else:
            raise TypeError("A supporting file in {} cannot be parsed".format(spec_id))

        with open(os.path.join(supporting_dir, spec_id, in_name), 'rb') as infile:
            contents = infile.read()
        with open(os.path.join(cwd, out_name), 'wb') as outfile:
            outfile.write(contents)
            written_files.append(out_name)

    return supporting_dir, written_files


def remove_supporting(written_files):
    try:
        for supporting_file in written_files:
            os.remove(supporting_file)
    except FileNotFoundError:
        pass
