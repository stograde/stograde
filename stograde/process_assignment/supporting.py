import os
import shutil
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..specs.spec import Spec


def import_supporting(*, spec: 'Spec', basedir: str) -> Tuple[str, List[str]]:
    """Copy supporting and input files into student's homework directory"""
    cwd = os.getcwd()
    supporting_dir = os.path.join(basedir, 'data', 'supporting')
    written_files = []

    # write the supporting files into the folder
    for file in spec.supporting_files:
        shutil.copy(os.path.join(supporting_dir, spec.id, file.file_name),
                    os.path.join(cwd, file.destination))
        written_files.append(file.destination)

    return supporting_dir, written_files


def remove_supporting(written_files: List[str]):
    """Remove supporting and input files after testing is complete"""
    for supporting_file in written_files:
        try:
            os.remove(supporting_file)
        except FileNotFoundError:
            pass
