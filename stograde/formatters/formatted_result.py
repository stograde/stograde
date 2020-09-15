from dataclasses import dataclass

from stograde.formatters.format_type import FormatType


@dataclass
class FormattedResult:
    assignment: str
    content: str
    student: str
    type: 'FormatType'
