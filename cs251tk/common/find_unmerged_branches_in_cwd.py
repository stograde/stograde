from .run import run


# TODO: This is a bit slow. Look for a faster way to check.
def find_unmerged_branches_in_cwd():
    """Check for unmerged branches in the current repository"""
    _, unmerged_branches = run(['git', 'branch', '-a', '--no-merged', 'master'])
    unmerged_branches = [s.strip()
                         for s in unmerged_branches.split('\n')
                         if s.strip()]
    return unmerged_branches
