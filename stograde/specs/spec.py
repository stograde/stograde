from dataclasses import dataclass, field
import os
from typing import List, TYPE_CHECKING, Optional
import yaml

from .spec_file import create_spec_file
from .supporting_file import create_supporting_file

if TYPE_CHECKING:
    from .spec_file import SpecFile
    from .supporting_file import SupportingFile


@dataclass
class Spec:
    id: str
    folder: str
    architecture: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    files: List['SpecFile'] = field(default_factory=list)
    supporting_files: List['SupportingFile'] = field(default_factory=list)


def create_spec(yaml_path: str, basedir: str) -> Spec:
    with open(os.path.join(basedir, yaml_path), 'r', encoding='utf-8') as yaml_file:
        loaded_file = yaml.safe_load(yaml_file)

    assert 'assignment' in loaded_file

    # assignment id and folder
    new_spec = Spec(id=loaded_file['assignment'],
                    folder=loaded_file.get('folder', loaded_file['assignment']))

    # assignment files
    if loaded_file.get('files', None) is not None:
        for file in loaded_file['files']:
            file_spec = create_spec_file(file)

            if loaded_file.get('tests', None) is not None:
                file_spec.add_from_tests(loaded_file['tests'])

            new_spec.files.append(file_spec)

    # dependencies
    dependencies = loaded_file.get('dependencies', [])
    if isinstance(dependencies, str):
        dependencies = [dependencies]
    assert isinstance(dependencies, list)

    # supporting/input files
    if loaded_file.get('supporting', None) is not None:
        for s_file in loaded_file['supporting']:
            new_spec.supporting_files.append(create_supporting_file(s_file))

    if loaded_file.get('inputs', None) is not None:
        for i_file in loaded_file['inputs']:
            new_spec.supporting_files.append(create_supporting_file(i_file))

    return new_spec
