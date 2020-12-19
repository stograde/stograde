from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..process_file.compile_result import CompileResult
    from ..process_file.test_result import TestResult


@dataclass
class FileResult:
    """The results from compiling and testing an assignment file"""
    file_name: str  # Name of the file
    contents: str = ''  # Contents of the file
    compile_results: List['CompileResult'] = field(default_factory=list)  # Results of each compilation
    test_results: List['TestResult'] = field(default_factory=list)  # Results of each test
    file_missing: bool = False  # Is the file missing
    last_modified: str = ''  # Last modification date according to git
    other_files: List[str] = field(default_factory=list)  # Other files in the directory (used if file is missing)
    optional: bool = False  # Is the file not required to exist
    compile_optional: bool = False  # Is the file not required to compile
    truncated_after: Optional[int] = None  # How much were the file contents truncated
