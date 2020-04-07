from dataclasses import dataclass


@dataclass
class SupportingFile:
    file_name: str
    destination: str


def create_supporting_file(s_file_spec) -> SupportingFile:
    if isinstance(s_file_spec, dict):
        assert 'file' in s_file_spec
        file_name = s_file_spec['file']
        destination = s_file_spec.get('destination', file_name)
    elif isinstance(s_file_spec, list):
        file_name = s_file_spec[0]
        if len(s_file_spec) == 1:
            destination = s_file_spec[0]
        else:
            destination = s_file_spec[1]
    elif isinstance(s_file_spec, str):
        file_name = s_file_spec
        destination = s_file_spec
    else:
        raise TypeError('Cannot parse "inputs:" and/or "supporting:": incorrect data type for a file: {}'
                        .format(type(s_file_spec)))

    return SupportingFile(file_name=file_name,
                          destination=destination)
