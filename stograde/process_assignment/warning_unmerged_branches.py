from ..common import find_unmerged_branches_in_cwd
from ..student.student_result import StudentResult


def find_unmerged_branches(result: StudentResult):
    # approach taken from https://stackoverflow.com/a/3602022/2347774
    unmerged_branches = find_unmerged_branches_in_cwd()
    if unmerged_branches:
        result.unmerged_branches = unmerged_branches
