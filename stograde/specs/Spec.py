from dataclasses import dataclass
from typing import List

import yaml

from .Spec_File import SpecFile, create_spec_file
from .Supporting_File import SupportingFile, create_supporting_file


@dataclass
class Spec:
    id: str
    files: List[SpecFile] = List
    supporting_files: List[SupportingFile] = List


def create_spec(yaml_path: str) -> Spec:
    with open(yaml_path, 'r', encoding='utf-8') as yaml_file:
        loaded_file = yaml.safe_load(yaml_file)

    assert 'assignment' in loaded_file

    # assignment id
    new_spec = Spec(id=loaded_file['assignment'])

    # assignment files
    if loaded_file.get('files', None) is not None:
        for file in loaded_file['files']:
            file_spec = create_spec_file(file)

            if loaded_file.get('tests', None) is not None:
                file_spec.add_from_tests(loaded_file['tests'])

            new_spec.files += file_spec

    # supporting/input files
    if loaded_file.get('supporting', None) is not None:
        for s_file in loaded_file['supporting']:
            new_spec.supporting_files += create_supporting_file(s_file)

    if loaded_file.get('inputs', None) is not None:
        for i_file in loaded_file['inputs']:
            new_spec.supporting_files += create_supporting_file(i_file)

    return new_spec
