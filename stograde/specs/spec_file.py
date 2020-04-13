from dataclasses import dataclass
from typing import List

from .file_options import FileOptions


@dataclass
class SpecFile:
    file_name: str
    compile_commands: List[str]
    test_commands: List[str]
    options: FileOptions

    def add_from_tests(self, test_specs: list):
        """Support legacy specs with a separate `tests:` tag

        :param test_specs: The `list` under `tests:`
        """

        test_commands = []

        for file_test_spec in test_specs:
            if isinstance(file_test_spec, dict):
                if file_test_spec.get('file') == self.file_name:
                    commands = file_test_spec.get('commands', [])
                    if isinstance(commands, str):
                        commands = [commands]
                    test_commands += commands

            elif isinstance(file_test_spec, list):  # legacy spec support
                if len(file_test_spec) == 1:
                    continue
                elif file_test_spec[0] == self.file_name:
                    test_commands += [f for f in file_test_spec[1:] if isinstance(f, str)]

            else:
                raise TypeError('Cannot parse "tests:": incorrect data type for a test: {}'
                                .format(type(file_test_spec)))

        self.test_commands.extend(test_commands)

        return self


def create_spec_file(file_spec) -> SpecFile:
    """Create a new SpecFile instance

    :param file_spec: A `dict` or `list` with the file specifications
    """

    if isinstance(file_spec, dict):
        assert 'file' in file_spec
        file_name = file_spec['file']

        compile_commands = file_spec.get('commands', [])
        if isinstance(compile_commands, str):
            compile_commands = [compile_commands]
        assert isinstance(compile_commands, list)

        test_commands = file_spec.get('tests', [])
        if isinstance(test_commands, str):
            test_commands = [test_commands]
        assert isinstance(test_commands, list)

        file_options = file_spec.get('options', {})
        options = FileOptions().update(file_options)

    elif isinstance(file_spec, list):  # legacy spec support
        file_name = file_spec[0]
        compile_commands = [f for f in file_spec[1:] if isinstance(f, str)]
        test_commands = []
        option_list = [opt for opt in file_spec[1:] if isinstance(opt, dict)]
        option_dict = {k: v for opt in option_list for k, v in opt.items()}
        options = FileOptions().update(option_dict)

    else:
        raise TypeError('Cannot parse "files:": incorrect data type for a file: {}'.format(type(file_spec)))

    return SpecFile(file_name=file_name,
                    compile_commands=compile_commands,
                    test_commands=test_commands,
                    options=options)
