"""Deal with argument parsing for Referee"""

import argparse
import sys
import json


def get_args():
    """Construct the argument list and parse the passed arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='data', nargs='?')
    parser.add_argument('--stdin', action='store_true', help='read from stdin')
    parser.add_argument('--debug', action='store_true', help='enable debugging mode (throw errors, etc)')
    parser.add_argument('--send', action='store_true', help='actually send emails')

    # parser.add_argument('STOGIT_URL', help='The stogit base URL')
    # parser.add_argument('USERNAME', help='Which student to process')
    # parser.add_argum?ent('COMMIT', nargs='+', help='Commit hashes to process')

    return parser


def process_args():
    """Process the arguments and create usable data from them"""
    parser = get_args()
    args = vars(parser.parse_args())
    if args['stdin']:
        args['data'] = sys.stdin.read()
    args['data'] = json.loads(args['data'])
    return args
