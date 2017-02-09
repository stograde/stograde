from argparse import Namespace
from .args import get_args, massage_args


def test_get_args():
    parser = get_args()

    def args(arglist):
        return vars(parser.parse_args(arglist))

    assert type(parser.parse_args([])) == Namespace
    assert args([]) == {
        'all': False,
        'clean': False,
        'date': None,
        'debug': False,
        'gist': False,
        'input': [],
        'no_check': False,
        'no_progress': False,
        'no_update': False,
        'partials': False,
        'quiet': False,
        'record': [],
        'section': [],
        'sort': 'name',
        'stogit': 'git@stogit.cs.stolaf.edu:sd-s17',
        'students': [],
        'workers': 8,
    }

    assert args(['--all'])['all'] is True
    assert args(['-w4'])['workers'] == 4
    assert args(['--no-progress'])['no_progress'] is True
    assert args(['--record', 'hw4'])['record'] == [['hw4']]
    assert args(['--record', 'hw4', '--record', 'hw5'])['record'] == [['hw4'], ['hw5']]


def test_massage_args():
    parser = get_args()

    def args(arglist):
        return vars(parser.parse_args(arglist))

    students = {
        'my': ['rives'],
    }

    assert massage_args(args([]), students) == {
        'all': False,
        'clean': False,
        'date': None,
        'debug': False,
        'gist': False,
        'input': [],
        'no_check': False,
        'no_progress': False,
        'no_update': False,
        'partials': False,
        'quiet': False,
        'record': [],
        'section': ['my'],
        'sort': 'name',
        'stogit': 'git@stogit.cs.stolaf.edu:sd-s17',
        'students': ['rives'],
        'workers': 8,
    }

    assert massage_args(args(['--record', 'hw4']), students)['record'] == ['hw4']
