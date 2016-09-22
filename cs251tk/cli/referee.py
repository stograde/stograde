import sys
from os import getcwd

from cs251tk.referee import process_student
from cs251tk.referee import process_args
from cs251tk.common import flatten
from cs251tk.common import chdir
from cs251tk.common import parse_commit_msg_for_assignments
from cs251tk.specs import load_some_specs
from tempfile import gettempdir


def parse_commits_for_assignments(commits):
    """Takes a list of commits and returns the affected assignments

    Input is a commit message; it returns a list of (hw|lab, ##) tuples.

    A commit looks like the following:

    {
      "id": "b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
      "message": "Update Catalan translation to e38cb41.",
      "timestamp": "2011-12-12T14:27:31+02:00",
      "url": "http://example.com/mike/diaspora/commit/b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
      "author": {
        "name": "Jordi Mallach",
        "email": "jordi@softcatala.org"
      },
      "added": ["CHANGELOG"],
      "modified": ["app/controller/application.rb"],
      "removed": []
    }

    Tested on these commit messages:
        - 'hw13 complete; part of hw14'
        - [more messages in test/assignment_parsing_test]
    """
    return set(flatten([parse_commit_msg_for_assignments(c['message']) for c in commits]))


def send_recordings(*args):
    print(*args)


def main():
    args = process_args()
    basedir = getcwd()

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
    print(affected_assignments)

    stringified_assignments = [''.join(pair) for pair in affected_assignments]
    specs = load_some_specs(stringified_assignments)
    if not specs:
        print('no specs loaded!')
        sys.exit(1)

    # ensure that two runs of referee with the same repo don't interfere with each other
    with chdir(gettempdir()):
        results, recordings = process_student(repo=repo,
                                              branch=branch,
                                              assignments=stringified_assignments,
                                              folder=repo_folder,
                                              specs=specs,
                                              basedir=basedir,
                                              debug=args['debug'])

        send_recordings(name, email, results, recordings)
