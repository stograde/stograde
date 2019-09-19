import os


def import_supporting(*, spec, spec_id, basedir):
    cwd = os.getcwd()
    inputs = spec.get('inputs', [])
    supporting_dir = os.path.join(basedir, 'data', 'supporting')
    written_files = []

    # write the supporting files into the folder
    for filename in inputs:
        if isinstance(filename, list):
            if len(filename) == 1:
                in_name = filename[0]
                out_name = filename[0]
            else:
                in_name = filename[0]
                out_name = filename[1]
        else:
            in_name = filename
            out_name = filename

        with open(os.path.join(supporting_dir, spec_id, in_name), 'rb') as infile:
            contents = infile.read()
        with open(os.path.join(cwd, out_name), 'wb') as outfile:
            outfile.write(contents)
            written_files.append(out_name)

    return supporting_dir, written_files


def remove_supporting(written_files):
    try:
        for inputfile in written_files:
            os.remove(inputfile)
    except FileNotFoundError:
        pass
