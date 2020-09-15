import html
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


def format_assignment_html(result: 'RecordResult') -> 'FormattedResult':
    """Given a single recording, format it into an HTML file.

    Each recording will only have one student.
    """

    try:
        files = format_files_list(result.file_results)
        warnings = format_warnings(result.warnings)
        header = format_header(result, warnings)
        output = (header + files) + '\n<hr>\n'

    except Exception as err:
        if global_vars.DEBUG:
            raise err
        output = format_as_code(traceback.format_exc())

    return FormattedResult(assignment=result.spec_id,
                           content=output,
                           student=result.student,
                           type=FormatType.HTML)


def format_files_list(files: List['FileResult']) -> str:
    return '\n\n'.join([format_file(info) for info in files])


def format_header(result: 'RecordResult', warnings: str) -> str:
    """Format the header for the section of the log file"""

    header = '<h1 id="{student}">{spec} - {student}</h1>\n'.format(spec=result.spec_id,
                                                                   student=result.student)

    if not result.warnings.assignment_missing:
        first_submit = '<p><b>First submission for {}: {}</b></p>'.format(result.spec_id, result.first_submission)
        header += first_submit + '\n'

    if warnings:
        header += warnings + '\n'

    return header + '\n'


def format_warnings(warnings: 'SubmissionWarnings') -> str:
    if warnings.assignment_missing:
        return '<p><b>No submission found</b></p>\n'

    elif warnings.unmerged_branches:
        return '<p><b>Repository has unmerged branches:</b></p>\n{}'.format(format_as_ul(warnings.unmerged_branches))

    elif warnings.recording_err:
        return '<p><b>Warning: ' + warnings.recording_err + '</b></p>'

    else:
        return ''


def format_file(file_info: 'FileResult') -> str:
    """Format a file for the log.
    Formats and concatenates a header, the file contents, compile output and test output.

    Last modification is calculated and added to header.
    If file does not exist, adds a list of all files in the directory.
    If file is missing and is optional, adds a note
    """

    contents = format_file_contents(file_info.contents) + '\n'
    compilation = format_file_compilation(file_info.compile_results) + '\n'
    test_results = format_file_tests(file_info.test_results) + '\n'

    if file_info.last_modified:
        last_modified = ' ({})'.format(file_info.last_modified)
    else:
        last_modified = ''

    file_header = '<h2><code>{}</code>{}</h2>\n'.format(file_info.file_name, last_modified)

    if file_info.file_missing:
        note = '<p>File not found. <code>ls .</code> says that these files exist:</p>'
        directory_listing = format_as_code('\n'.join(file_info.other_files))

        if file_info.optional:
            file_header = file_header.strip()
            file_header = file_header[:-5] + ' (<b>optional submission</b>)</h2>\n'

        return '\n'.join([file_header, note, directory_listing + '\n\n'])

    return '\n'.join([file_header, contents, compilation, test_results])


def format_file_contents(contents: str):
    """Add code block around file contents.

    If a file is empty or contains only whitespace, note this in the log.
    """
    if not contents.rstrip():
        return '<p><i>File empty</i></p>'
    return format_as_code(contents)


def format_file_compilation(compilations: List['CompileResult']) -> str:
    """Add header and code block to compile command outputs"""

    result = []
    for compile_result in compilations:
        output = compile_result.output
        command = '<code>{command}</code>'.format(command=html.escape(compile_result.command))

        if not output:
            result.append('<p><b>no warnings: {}</b></p>\n'.format(command))
        else:
            result.append('<p><b>warnings: {}</b></p>'.format(command))
            result.append(format_as_code(output) + '\n')

    return '\n'.join(result)


def format_file_tests(test_results: List['TestResult']) -> str:
    """Add header and markdown code block to test outputs"""

    result = []
    for test in test_results:
        header = '<p><b>results of <code>{}</code></b> (status: {})</p>\n'.format(test.command,
                                                                                            test.status.name)
        if test.output:
            header_and_contents = header + format_as_code(test.output) + '\n'
            if test.truncated:
                header_and_contents += '<p><i>(truncated after {} lines)</i></p>\n'.format(test.truncated_after)
            result.append(header_and_contents)
        else:
            result.append(header)

    return '\n'.join(result)


def format_as_code(data: str) -> str:
    if not data:
        return ''
    return '<pre><code>\n{}\n</code></pre>'.format(html.escape(data))


def format_as_ul(data: List[str]) -> str:
    if not data:
        return ''
    return '<ul>\n<li>{}</li>\n</ul>'.format('</li>\n<li>'.join(data))
