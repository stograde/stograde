from cs251tk.common import chdir
from cs251tk.common import run


def checkout_date(student, date=None):
    if date:
        with chdir(student):
            rev_list = ['git', 'rev-list', '-n', '1', '--before="{} 18:00"'.format(date), 'master']
            _, rev = run(rev_list)
            run(['git', 'checkout', rev, '--force', '--quiet'])


def checkout_ref(student, ref):
    with chdir(student):
        run(['git', 'checkout', ref, '--force', '--quiet'])
