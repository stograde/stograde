"""Deal with argument parsing for Referee"""

import argparse


def get_args():
    """Construct the argument list and parse the passed arguments"""
    parser = argparse.ArgumentParser(description='''
    Example:
        referee git@stogit.cs.stolaf.edu:sd-f16 rives 14179e9
    ''')

    parser.add_argument('STOGIT_URL', help='The stogit base URL')
    parser.add_argument('USERNAME', help='Which student to process')
    parser.add_argument('COMMIT', nargs='+', help='Commit hashes to process')

    return parser


def process_args():
    """Process the arguments and create usable data from them"""
    parser = get_args()
    args = vars(parser.parse_args())
    return args
