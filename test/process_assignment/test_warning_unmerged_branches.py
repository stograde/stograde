from stograde.process_assignment.warning_unmerged_branches import find_unmerged_branches
from stograde.student.student_result import StudentResult
from test.utils import git, touch


def test_find_unmerged_branches(tmpdir):
    student_result = StudentResult('student1')

    with tmpdir.as_cwd():
        git('init')
        git('symbolic-ref', 'HEAD', 'refs/heads/main')  # Workaround for older versions of git without default main
        git('config', 'user.email', 'an_email@email_provider.com')
        git('config', 'user.name', 'Some Random Name')

        touch('file1')
        git('add', 'file1')
        git('commit', '-m', 'initial')

        git('checkout', '-b', 'branch')

        touch('file2')
        git('add', 'file2')
        git('commit', '-m', 'newcommit')

        git('checkout', 'main')

        find_unmerged_branches(student_result)

    assert student_result.unmerged_branches == ['branch']
