import traceback
from typing import List, TYPE_CHECKING

from .format_type import FormatType
from .formatted_result import FormattedResult
from ..toolkit import global_vars

if TYPE_CHECKING:
    from ..process_assignment.record_result import RecordResult
    from ..process_assignment.submission_warnings import SubmissionWarnings
    from ..process_file.compile_result import CompileResult
    from ..process_file.file_result import FileResult
    from ..process_file.test_result import TestResult


def format_assignment_markdown(result: 'RecordResult') -> 'FormattedResult':
    """Given a single recording, format it into a Markdown file.

    Each recording will only have one student.
    """

    try:
        files = format_files_list(result.file_results)
        warnings = format_warnings(result.warnings)
        header = format_header(result, warnings)
        output = (header + files) + '\n\n'

    except Exception as err:
        if global_vars.DEBUG:
            raise err
        output = '```\n' + traceback.format_exc() + '\n```\n'

    return FormattedResult(assignment=result.spec_id,
                           content=output,
                           student=result.student,
                           type=FormatType.MD)


def format_files_list(files: List['FileResult']) -> str:
    return '\n\n' + '\n\n'.join([format_file(info) for info in files])


def format_header(result: 'RecordResult', warnings: str) -> str:
    """Format the header for the section of the log file"""

    header = '# {spec} – {student}\n'.format(spec=result.spec_id,
                                             student=result.student)

    if not result.warnings.assignment_missing:
        first_submit = 'First submission for {}: {}'.format(result.spec_id, result.first_submission)
        header += first_submit + '\n'

    if warnings:
        header += '\n' + warnings + '\n'

    return header


def format_warnings(warnings: 'SubmissionWarnings') -> str:
    if warnings.assignment_missing:
        return '**No submission found**\n'

    elif warnings.unmerged_branches:
        branches = ['- ' + b for b in warnings.unmerged_branches]
        return '### *Repository has unmerged branches:*\n{}'.format('\n'.join(branches))

    elif warnings.recording_err:
        return '**Warning: ' + warnings.recording_err + '**'

    else:
        return ''


def format_file(file_info: 'FileResult') -> str:
    """Format a file for the log.
    Formats and concatenates a header, the file contents, compile output and test output.

    Last modification is calculated and added to header.
    If file does not exist, adds a list of all files in the directory.
    If file is missing and is optional, adds a note
    """

    contents = format_file_contents(file_info)
    compilation = format_file_compilation(file_info.compile_results)
    test_results = format_file_tests(file_info.test_results)

    if file_info.last_modified:
        last_modified = ' ({})'.format(file_info.last_modified)
    else:
        last_modified = ''

    if file_info.actual_name is not None:
        file_header = '## {} (alternate name for {}){}\n'.format(file_info.actual_name,
                                                                 file_info.file_name,
                                                                 last_modified)
    else:
        file_header = '## {}{}\n'.format(file_info.file_name, last_modified)

    if file_info.file_missing:
        note = 'File not found. `ls .` says that these files exist:'
        directory_listing = '```\n' + '\n'.join(file_info.other_files) + '\n```\n'

        if file_info.optional:
            file_header = file_header.strip()
            file_header += ' (**optional submission**)\n'

        return '\n'.join([file_header, note, directory_listing])

    if file_info.other_files:
        file_header = file_header + '*Alternate files detected:*\n- ' + '\n- '.join(file_info.other_files) + '\n'

    return '\n'.join([file_header, contents, compilation, test_results])


def get_file_extension(filename: str) -> str:
    """Returns the file extension if there is one"""
    if '.' in filename:
        return filename.split('.')[-1]
    else:
        return ''


def format_file_contents(file_info: 'FileResult') -> str:
    """Add markdown code block around file contents with extension for code highlighting.

    If a file is empty or contains only whitespace, note this in the log.
    """

    if not file_info.contents.rstrip():
        return '*File empty*'

    contents = '```{}\n'.format(get_file_extension(file_info.file_name)) + file_info.contents + '\n```\n'

    if file_info.truncated_after:
        contents += '*(truncated after {} chars)*\n'.format(file_info.truncated_after)

    return contents


def format_file_compilation(compilations: List['CompileResult']) -> str:
    """Add header and markdown code block to compile command outputs"""

    result = []
    for compile_result in compilations:
        output = compile_result.output
        command = '`{command}`'.format(command=compile_result.command)

        if not output:
            result.append('**no warnings: {}**\n'.format(command))
        else:
            result.append('**warnings: {}**\n'.format(command))
            result.append('```\n' + output + '\n```\n')
            if compile_result.truncated_after:
                result.append('*(truncated after {} chars)*\n'.format(compile_result.truncated_after))

    return '\n'.join(result)


def format_file_tests(test_results: List['TestResult']) -> str:
    """Add header and markdown code block to test outputs"""

    result = []
    for test in test_results:
        header = '**results of `{command}`** (status: {status})\n'.format(command=test.command,
                                                                          status=test.status.name)
        if test.output:
            header_and_contents = header + '\n```\n' + test.output + '\n```\n'
            if test.truncated_after:
                header_and_contents += '*(truncated after {} chars)*\n'.format(test.truncated_after)
            result.append(header_and_contents)
        else:
            result.append(header)

    return '\n'.join(result)
