from stograde.common import find_unmerged_branches_in_cwd
from . import Record_Result


def find_unmerged_branches(result: Record_Result):
    # approach taken from https://stackoverflow.com/a/3602022/2347774
    unmerged_branches = find_unmerged_branches_in_cwd()
    if unmerged_branches:
        result.warnings.unmerged_branches = unmerged_branches
