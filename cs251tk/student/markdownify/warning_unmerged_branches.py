from cs251tk.common import find_unmerged_branches_in_cwd


def find_unmerged_branches():
    # approach taken from https://stackoverflow.com/a/3602022/2347774
    unmerged_branches = find_unmerged_branches_in_cwd()
    if not unmerged_branches:
        return False

    return unmerged_branches
