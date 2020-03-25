import os
from typing import List, Tuple

from ..specs.spec import Spec


def import_supporting(*,
                      spec: Spec,
                      basedir: str) -> Tuple[str, List[str]]:
    cwd = os.getcwd()
    supporting_dir = os.path.join(basedir, 'data', 'supporting')
    written_files = []

    # write the supporting files into the folder
    for file in spec.supporting_files:
        with open(os.path.join(supporting_dir, spec.id, file.file_name), 'rb') as infile:
            contents = infile.read()
        with open(os.path.join(cwd, file.destination), 'wb') as outfile:
            outfile.write(contents)
            written_files.append(file.destination)

    return supporting_dir, written_files


def remove_supporting(written_files):
    try:
        for supporting_file in written_files:
            os.remove(supporting_file)
    except FileNotFoundError:
        pass

