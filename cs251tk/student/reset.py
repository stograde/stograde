
def reset(student, args):
    with chdir(student):
        if args['day']:
            run(['git', 'checkout', 'master', '--quiet', '--force'])
