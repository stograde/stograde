from typing import List

from .run import run


# TODO: This is a bit slow. Look for a faster way to check.
def find_unmerged_branches_in_cwd() -> List[str]:
    """Check for unmerged branches in the current repository"""
    _, unmerged_branches, _ = run(['git', 'branch', '-a', '--no-merged', 'main'])
    return [s.strip()
            for s in unmerged_branches.split('\n')
            if s.strip() and 'not a git repository' not in s]
