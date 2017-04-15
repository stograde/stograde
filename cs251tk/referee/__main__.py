from tempfile import gettempdir
import logging
import sys
import os

from ..common import chdir
from ..specs import load_some_specs
from .args import process_args
from .process_student import process_student
from .parse_commits import parse_commits_for_assignments
from .emailify import emailify
from .send_email import send_email
from collections import Counter


def parse_gitlab6_webhook(payload):
    emails = [c['author']['email'] for c in payload['commits']]
    most_common_email = Counter(emails).most_common(1)[0][0]

    return {
        'name': payload['user_name'],
        'email': most_common_email,
        'branch': payload['ref'],
        'repo': payload['repository']['url'],
        'commits': payload['commits'],
        'repo_folder': str(payload['user_id']),
    }


def parse_gitlab9_webhook(payload):
    if payload['object_kind'] != 'push':
        raise Exception('Not a push event!')

    return {
        'name': payload['user_name'],
        'email': payload['user_email'],
        'branch': payload['ref'],
        'repo': payload['project']['git_ssh_url'],
        'commits': payload['commits'],
        'repo_folder': payload['project']['path_with_namespace'].split('/')[-1],
    }


def main():
    args = process_args()
    basedir = os.getcwd()

    logging.basicConfig(level=logging.DEBUG if args['debug'] else logging.WARNING)

    payload = args['data']

    print(payload)

    parsed_payload = {}
    try:
        parsed_payload = parse_gitlab6_webhook(payload)
    except KeyError:
        parsed_payload = parse_gitlab9_webhook(payload)

    print(parsed_payload)

    name = parsed_payload['name']
    email = parsed_payload['email']
    branch = parsed_payload['branch']
    repo = parsed_payload['repo']
    commits = parsed_payload['commits']
    repo_folder = parsed_payload['repo_folder']

    print('processing {}#{}'.format(repo, branch))
    print('author: {} <{}>'.format(name, email))
    print('destination: {}'.format(repo_folder))

    print('before push', payload['before'])
    print('after push', payload['after'])

    affected_assignments = parse_commits_for_assignments(commits)

    stringified_assignments = [''.join(pair) for pair in affected_assignments]
    print(stringified_assignments)

    specs = load_some_specs(stringified_assignments, basedir='./data')
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

    email_blob = emailify(recordings=recordings,
                          name=name,
                          to=email,
                          debug=args['debug'])

    if args['send']:
        send_email(email_blob)
        print('email sent')
    else:
        print('Not sending email: no --send flag')
        print()
        print(email_blob)
