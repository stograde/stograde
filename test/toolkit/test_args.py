from stograde.toolkit.args import build_argparser


def args(arglist):
    return vars(build_argparser().parse_args(args=arglist))
