from dataclasses import dataclass
from typing import Optional


@dataclass(eq=True, frozen=True)
class DriveResult:
    """The metadata for an assignment file shared via Google Drive"""
    student_email: str
    file_name: Optional[str]
    create_time: Optional[str]
    url: Optional[str]
