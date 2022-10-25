import functools
import os
from PyInquirer import prompt, style_from_dict, Token
from typing import List, TYPE_CHECKING

from . import server
from ..common import chdir
from ..process_assignment import import_supporting, remove_supporting
from ..process_file import process_file
from ..process_file.file_result import FileResult
from ..process_file.process_file import get_file
from ..toolkit.process_parallel import process_parallel
from ..student.process_student import prepare_student

if TYPE_CHECKING:
    from ..specs.spec import Spec


def launch_cli(base_dir: str,
               branch: str,
               clean: bool,
               date: str,
               no_progress_bar: bool,
               skip_repo_update: bool,
               spec: 'Spec',
               stogit_url: str,
               students: List[str],
               workers: int):
    """Start the web grading CLI"""
    with chdir(os.path.join(base_dir, 'students')):
        usernames = [
            '{} NO SUBMISSION'.format(student)
            if not os.path.exists('{}/{}'.format(student, spec.id))
            else student
            for student in students
        ]

        print('Loading repos. Please wait...')

        single_repo = functools.partial(
            prepare_student,
            stogit_url=stogit_url,
            branch=branch,
            do_clean=clean,
            do_clone=not skip_repo_update,
            do_pull=not skip_repo_update,
            do_checkout=True,
            date=date)

        process_parallel(students=students,
                         no_progress_bar=no_progress_bar,
                         workers=workers,
                         operation=single_repo)

        while True:
            student = ask_student(usernames)

            if not student or student == 'QUIT':
                return
            elif 'NO SUBMISSION' in student:
                continue

            files = check_student(student, spec, base_dir)

            if files:
                ask_file(files, student, spec, base_dir)


def ask_student(usernames: List[str]) -> str:
    """Ask user to select a student"""
    style = style_from_dict({
        Token.QuestionMark: '#959ee7 bold',
        Token.Selected: '#959ee7',
        Token.Pointer: '#959ee7 bold',
        Token.Answer: '#959ee7 bold',
    })
    questions = [
        {
            'type': 'list',
            'name': 'student',
            'message': 'Choose student',
            'choices': ['QUIT', *usernames],
        }
    ]

    student = prompt(questions, style=style)

    if not student:
        return ''

    return student['student']


def check_student(student: str,
                  spec: 'Spec',
                  base_dir: str):
    """Process student's files and populate file list"""
    files = []
    if os.path.exists('{}/{}'.format(student, spec.id)):
        print('Processing...')
        with chdir('{}/{}'.format(student, spec.id)):
            # prepare the current folder
            supporting_dir, written_files = import_supporting(spec=spec,
                                                              basedir=base_dir)

            for file in spec.files:
                if file.options.web_file:
                    result = FileResult(file_name=file.file_name)
                    exists = get_file(file_spec=file,
                                      file_result=result)

                    description = file.file_name

                    if not exists:
                        if result.optional:
                            description = '{} MISSING (OPTIONAL)'.format(file.file_name)
                        else:
                            description = '{} MISSING'.format(file.file_name)

                    files = files + [description]
            # and we remove any supporting files
            remove_supporting(written_files)

    return files


def ask_file(files: List[str],
             student: str,
             spec: 'Spec',
             basedir: str):
    """Ask user to select a file to view"""
    style = style_from_dict({
        Token.QuestionMark: '#e3bd27 bold',
        Token.Selected: '#e3bd27',
        Token.Pointer: '#e3bd27 bold',
        Token.Answer: '#e3bd27 bold',
    })

    while True:
        questions = [
            {
                'type': 'list',
                'name': 'file',
                'message': 'Choose file',
                'choices': ['BACK', *files],
            }
        ]
        file = prompt(questions, style=style)

        # File has been selected so process and display it
        if file and file['file'] != 'BACK':
            file_spec = None
            for f in spec.files:
                if f.file_name == file['file']:
                    file_spec = f
                    break
            if file_spec:
                with chdir('{}/{}'.format(student, spec.id)):
                    # prepare the current folder
                    supporting_dir, written_files = import_supporting(spec=spec,
                                                                      basedir=basedir)
                    process_file(file_spec=file_spec,
                                 supporting_dir=supporting_dir,
                                 interact=False,
                                 skip_web_compile=False)

                    server.work_dir = os.getcwd()

                    # and we remove any supporting files
                    remove_supporting(written_files)

        else:
            return


def is_web_spec(spec: 'Spec') -> bool:
    """Check if the spec contains any web files"""
    web_spec = False
    for file in spec.files:
        if file.options.web_file:
            web_spec = True
            break
    return web_spec
