from tempfile import gettempdir
import sys
import os

from ..common import chdir
from ..specs import load_some_specs
from .args import process_args
from .process_student import process_student
from .parse_commits import parse_commits_for_assignments
from .emailify import emailify
from .send_email import send_email


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

    print('processing', repo)
    print('before', payload['before'])
    print('after', payload['after'])

    affected_assignments = parse_commits_for_assignments(commits)

    stringified_assignments = [''.join(pair) for pair in affected_assignments]

    specs = load_some_specs(stringified_assignments)
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

    print('processing complete')

    email_blob = emailify(recordings, name, to=email, debug=args['debug'])

    if args['send']:
        send_email(email_blob)
        print('email sent')
    else:
        print('Not sending email: no --send flag')
        print()
        print(email_blob)
