import os
import sys
from typing import List, TYPE_CHECKING

from .filter_specs import filter_loaded_specs, get_spec_paths
from .spec import create_spec
from ..common import chdir
from ..common.run import run
from ..common.run_status import RunStatus

if TYPE_CHECKING:
    from .spec import Spec


def load_specs(wanted_specs: List[str], data_dir: str, skip_spec_update: bool = False) -> List['Spec']:
    """Load the desired specs from the specs/ directory, filtering out any that are missing

    data/ directory should exist by this point with a repository
    """
    if not skip_spec_update:
        check_for_spec_updates(data_dir)

    # the repo has a /specs directory
    spec_dir = os.path.join(data_dir, 'specs')

    specs_to_load = get_spec_paths(wanted_specs, spec_dir)

    loaded_specs = [create_spec(filename, spec_dir) for filename in specs_to_load]  # Create list of Specs
    loaded_specs = filter_loaded_specs(loaded_specs)

    return loaded_specs


def check_for_spec_updates(data_dir: str):
    """Check if the specs have any updates using git fetch"""
    with chdir(data_dir):
        res, _, _ = run(['git', 'fetch', 'origin'])

        if res is not RunStatus.SUCCESS:
            print("Error fetching specs", file=sys.stderr)

        _, out, _ = run(['git', 'log', 'HEAD..origin/master'])

    if not out:
        return
    elif 'commit' in out:
        print("Spec updates found - Updating", file=sys.stderr)
        with chdir(data_dir):
            run(['git', 'pull', 'origin', 'master'])
    else:
        print("git log failed", file=sys.stderr)
