import sys
import os

from cs251tk.referee import process_student
from cs251tk.referee import process_args
from cs251tk.referee import parse_commits_for_assignments
from cs251tk.referee import send_recordings
from cs251tk.common import chdir
from cs251tk.specs import load_some_specs
from tempfile import gettempdir


def main():
    args = process_args()
    basedir = os.getcwd()

    payload = args['data']

    if payload['object_kind'] != 'push':
        sys.exit('Not a push event')

    name = payload['user_name']
    email = payload['user_email']

    branch = payload['ref']
    repo = payload['project']['git_ssh_url']
    commits = payload['commits']
    repo_folder = payload['project']['path_with_namespace'].split('/')[-1]

    affected_assignments = parse_commits_for_assignments(commits)

    stringified_assignments = [''.join(pair) for pair in affected_assignments]
    # print(sorted(stringified_assignments))
    specs = load_some_specs(stringified_assignments, basedir)
    if not specs:
        print('no specs loaded!')
        sys.exit(1)

    # ensure that two runs of referee with the same repo don't interfere with each other
    with chdir(gettempdir()):
        # print('working in', os.getcwd())
        results, recordings = process_student(repo=repo,
                                              branch=branch,
                                              assignments=stringified_assignments,
                                              folder=repo_folder,
                                              specs=specs,
                                              basedir=basedir,
                                              debug=args['debug'])

        send_recordings(recordings, name, email, debug=args['debug'])
