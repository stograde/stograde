from textwrap import indent
import traceback
from typing import Dict, List

from ..process_assignment.record_result import RecordResult
from ..process_assignment.submission_warnings import SubmissionWarnings
from ..process_file.compile_result import CompileResult
from ..process_file.file_result import FileResult
from ..process_file.test_result import TestResult
from ..toolkit import global_vars


def format_assignment_markdown(result: RecordResult) -> Dict:
    """Given a single recording, format it into a markdown file.

    Each recording will only have one student.

    Returns a {content: str, student: str, type: str, assignment: str} dict.
    """

    try:
        files = format_files_list(result.file_results)
        warnings = format_warnings(result.warnings)
        header = format_header(result, warnings)
        output = (header + files) + '\n\n'

    except Exception as err:
        if global_vars.DEBUG:
            raise err
        output = indent(traceback.format_exc(), ' ' * 4) + '\n\n'

    return {
        'assignment': result.spec_id,
        'content': output,
        'student': result.student,
        'type': 'md',
    }


def format_files_list(files) -> str:
    return '\n\n' + '\n\n'.join([format_file(info) for info in files])


def format_header(result: RecordResult, warnings: str) -> str:
    """Format the header for the section of the log file"""

    header = '# {spec} – {student}\n{first_submit}\n'.format(spec=result.spec_id,
                                                             student=result.student,
                                                             first_submit=result.first_submission)

    if warnings:
        header += '\n' + warnings + '\n'

    return header


def format_warnings(warnings: SubmissionWarnings) -> str:
    if warnings.assignment_missing:
        return '**No submission found**\n'

    elif warnings.unmerged_branches:
        branches = ['  - ' + b for b in warnings.unmerged_branches]
        return '### *Repository has unmerged branches:*\n{}'.format('\n'.join(branches))

    elif warnings.recording_err:
        return '**Warning: ' + warnings.recording_err + '**'

    else:
        return ''


def format_file(file_info: FileResult) -> str:
    """Format a file for the log.
    Formats and concatenates a header, the file contents, compile output and test output.

    Last modification is calculated and added to header.
    If file does not exist, adds a list of all files in the directory.
    If file is missing and is optional, adds a note in place of last modification time.
    """

    contents = format_file_contents(file_info.contents, file_info.file_name) + '\n'
    compilation = format_file_compilation(file_info.compile_results) + '\n'
    test_results = format_file_results(file_info.test_results) + '\n'

    if file_info.last_modified:
        last_modified = ' ({})'.format(file_info.last_modified)
    else:
        last_modified = ''

    file_header = '## {}{}\n'.format(file_info.file_name, last_modified)

    if file_info.file_missing:
        note = 'File not found. `ls .` says that these files exist:\n'
        directory_listing = indent('\n'.join(file_info.other_files), ' ' * 4)

        if file_info.optional:
            file_header = file_header.strip()
            file_header += ' (**optional submission**)\n'

        return '\n'.join([file_header, note, directory_listing + '\n\n'])

    return '\n'.join([file_header, contents, compilation, test_results])


def format_file_contents(contents: str, filename: str) -> str:
    """Add markdown code block around file contents with extension for code highlighting.

    If a file is empty or contains only whitespace, note this in the log.
    """

    if not contents.rstrip():
        return '*File empty*'
    return '```{}\n'.format(filename.split('.')[-1]) + contents + '\n```\n'


def format_file_compilation(compilations: List[CompileResult]) -> str:
    """Add header and markdown code block to compile command outputs"""

    result = []
    for compile_result in compilations:
        output = compile_result.output
        command = '`{command}`'.format(command=compile_result.command)

        if not output:
            result.append('**no warnings: {}**\n\n'.format(command))
        else:
            result.append('**warnings: {}**\n'.format(command))
            result.append('```\n' + output + '\n```\n')

    return '\n'.join(result)


def format_file_results(test_results: List[TestResult]) -> str:
    """Add header and markdown code block to test outputs"""

    result = []
    for test in test_results:
        header = '**results of `{command}`** (status: {status})\n'.format(command=test.command,
                                                                          status=test.status)
        if test.output:
            result.append(header + '\n```\n' + test.output + '\n```\n')
            if test.truncated:
                result.append('(truncated after {})'.format(test.truncated_after))
        else:
            result.append(header)

    return '\n'.join(result)
