from cs251tk.common import chdir
from cs251tk.common import run


def checkout_day(student, day=None):
    with chdir(student):
        if day:
            rev_list = ['git', 'rev-list', '-n', '1', '--before="{} 18:00"'.format(day), 'master']
            _, rev = run(rev_list)
            run(['git', 'checkout', rev, '--force', '--quiet'])


def checkout_ref(student, ref):
    with chdir(student):
        run(['git', 'checkout', ref, '--force', '--quiet'])
