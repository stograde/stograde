from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class DriveResult:
    student_email: str
    file_name: str
    create_time: str
    url: str
