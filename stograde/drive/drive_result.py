from dataclasses import dataclass
from typing import Optional


@dataclass(eq=True, frozen=True)
class DriveResult:
    student_email: str
    file_name: Optional[str]
    create_time: Optional[str]
    url: Optional[str]
