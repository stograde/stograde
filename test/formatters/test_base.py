from stograde.formatters import format_collected_data, markdown
from stograde.formatters.format_type import FormatType
from stograde.formatters.formatted_result import FormattedResult
from stograde.formatters.group_type import GroupType
from stograde.process_assignment.record_result import RecordResult
from stograde.process_assignment.submission_warnings import SubmissionWarnings
from stograde.student.student_result import StudentResult

student_results = [StudentResult(name='student',
                                 results=[RecordResult(spec_id='hw1',
                                                       student='student',
                                                       warnings=SubmissionWarnings(assignment_missing=True))]),
                   StudentResult(name='student2',
                                 results=[RecordResult(spec_id='lab1',
                                                       student='student2',
                                                       warnings=SubmissionWarnings(assignment_missing=True))]),
                   StudentResult(name='student3',
                                 results=[RecordResult(spec_id='hw1',
                                                       student='student3',
                                                       warnings=SubmissionWarnings(assignment_missing=True))]),
                   StudentResult(name='student',
                                 results=[RecordResult(spec_id='lab1',
                                                       student='student',
                                                       warnings=SubmissionWarnings(assignment_missing=True))])]


def test_format_collected_data_sort_assignment():
    results = format_collected_data(student_results=student_results,
                                    group_by=GroupType.ASSIGNMENT,
                                    formatter=markdown)

    assert results == {'hw1': [FormattedResult(assignment='hw1',
                                               content='# hw1 – student\n\n**No submission found**\n\n\n\n\n\n',
                                               student='student',
                                               type=FormatType.MD),
                               FormattedResult(assignment='hw1',
                                               content='# hw1 – student3\n\n**No submission found**\n\n\n\n\n\n',
                                               student='student3',
                                               type=FormatType.MD)],
                       'lab1': [FormattedResult(assignment='lab1',
                                                content='# lab1 – student2\n\n**No submission found**\n\n\n\n\n\n',
                                                student='student2',
                                                type=FormatType.MD),
                                FormattedResult(assignment='lab1',
                                                content='# lab1 – student\n\n**No submission found**\n\n\n\n\n\n',
                                                student='student',
                                                type=FormatType.MD)]}


def test_format_collected_data_sort_student():
    results = format_collected_data(student_results=student_results,
                                    group_by=GroupType.STUDENT,
                                    formatter=markdown)

    assert results == {'student': [FormattedResult(assignment='hw1',
                                                   content='# hw1 – student\n\n**No submission found**\n\n\n\n\n\n',
                                                   student='student',
                                                   type=FormatType.MD),
                                   FormattedResult(assignment='lab1',
                                                   content='# lab1 – student\n\n**No submission found**\n\n\n\n\n\n',
                                                   student='student',
                                                   type=FormatType.MD)],
                       'student2': [FormattedResult(assignment='lab1',
                                                    content='# lab1 – student2\n\n**No submission found**\n\n\n\n\n\n',
                                                    student='student2',
                                                    type=FormatType.MD)],
                       'student3': [FormattedResult(assignment='hw1',
                                                    content='# hw1 – student3\n\n**No submission found**\n\n\n\n\n\n',
                                                    student='student3',
                                                    type=FormatType.MD)]}


def test_format_collected_data_bad_sort():
    try:
        # noinspection PyTypeChecker
        format_collected_data([], None, markdown)
        raise AssertionError
    except TypeError:
        pass
