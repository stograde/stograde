from .run import run_command as run


def find_unmerged_branches_in_cwd():
    _, unmerged_branches = run(['git', 'branch', '-a', '--no-merged', 'master'])
    unmerged_branches = [s.strip()
                         for s in unmerged_branches.split('\n')
                         if s.strip()]
    return unmerged_branches
