from argparse import Namespace
from .args import get_args, massage_args


def test_get_args():
    parser = get_args()

    def args(arglist):
        return vars(parser.parse_args(arglist))

    assert type(parser.parse_args([])) == Namespace

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

    assert massage_args(args([]), students)['all'] == False
    assert massage_args(args([]), students)['section'] == ['my']
    assert massage_args(args([]), students)['students'] == ['rives']

    assert massage_args(args(['--record', 'hw4']), students)['record'] == ['hw4']
