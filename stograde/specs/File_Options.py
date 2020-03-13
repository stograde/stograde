from dataclasses import dataclass


@dataclass
class FileOptions:
    compile_optional: bool = False
    hide_contents: bool = False
    optional: bool = False
    timeout: int = 4
    truncate_contents: int = 10000
    truncate_output: int = 10000
    web_file: bool = False

    def update(self, options: dict):
        self.compile_optional = options.get('optional_compile', self.compile_optional)
        self.hide_contents = options.get('hide_contents', self.hide_contents)
        self.optional = options.get('optional', self.optional)
        self.timeout = options.get('timeout', self.timeout)
        self.truncate_contents = options.get('truncate_contents', self.truncate_contents)
        self.truncate_output = options.get('truncate_output', self.truncate_output)
        self.web_file = options.get('web', self.web_file)
