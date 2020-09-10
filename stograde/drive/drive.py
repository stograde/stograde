import datetime

from dateutil import tz
from dateutil.parser import parse
import os
import re
import sys
from typing import Any, Dict, List, Tuple

import dateutil
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .drive_result import DriveResult
from ..formatters.tabulate import JOIN, ROW
from ..process_assignment.assignment_type import AssignmentType, get_assignment_number, get_assignment_type


def authenticate() -> Credentials:
    if not os.path.exists('client_secret.json'):
        print('client_secret.json required for stograde drive functionality.', file=sys.stderr)
        print('Please make sure it is located in the directory you are running stograde in.', file=sys.stderr)
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json',
                                                     'https://www.googleapis.com/auth/drive.metadata.readonly')
    return flow.run_console()


def filter_file_shared_email(file: Dict[str, Any], email: str) -> bool:
    if 'permissions' not in file:
        return False
    for perm in file['permissions']:
        if 'emailAddress' in perm and perm['emailAddress'] == email:
            return True
    return False


def get_all_files(credentials: Credentials, email: str) -> List['DriveResult']:
    service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
    next_page_token = None
    all_user_files = []
    date = datetime.date.today()
    while True:
        response = service.files().list(q="modifiedTime > '{year}-{month}-01T00:00:00'"
                                        .format(year=date.year,
                                                month='01' if date.month < 7 else '07'),
                                        pageSize=100,
                                        fields='files(createdTime,name,owners,permissions,webViewLink),nextPageToken',
                                        pageToken=next_page_token).execute()
        all_user_files = all_user_files + [file for file in response['files']]
        next_page_token = response.get('nextPageToken', None)
        if next_page_token is None:
            break

    shared_files = list(filter(lambda f: filter_file_shared_email(f, email), all_user_files))

    return [DriveResult(student_email=file['owners'][0]['emailAddress'],
                        file_name=file['name'],
                        create_time=file['createdTime'],
                        url=file['webViewLink'])
            for file in shared_files]


def filter_file_assignment(file: 'DriveResult', assignment: str) -> bool:
    a_type = get_assignment_type(assignment)
    a_num = get_assignment_number(assignment)
    if a_type is AssignmentType.HOMEWORK:
        reg = '.*(hw|homework) ?' + str(a_num)
    elif a_type is AssignmentType.LAB:
        reg = '.*lab ?' + str(a_num)
    elif a_type is AssignmentType.WORKSHEET:
        reg = '.*(ws|worksheet) ?' + str(a_num)
    else:
        print('Could not parse assignment name {}'.format(assignment), file=sys.stderr)
        sys.exit(1)

    if re.match(reg, file.file_name, re.IGNORECASE):
        return True
    else:
        return False


def filter_files(files: List['DriveResult'], assignment: str) -> List['DriveResult']:
    return list(filter(lambda f: filter_file_assignment(f, assignment), files))


def group_files(files: List['DriveResult'],
                students: List[str]) -> Tuple[List['DriveResult'],
                                              List['DriveResult'],
                                              List['DriveResult']]:
    missing_students = [DriveResult(student + '@stolaf.edu', None, None, None) for student in
                        list(set(students).difference({file.student_email[:-11] for file in files}))]
    stolaf_files = [file for file in files if file.student_email.endswith('@stolaf.edu')]
    stolaf_class_files = [file for file in files if file.student_email[:-11] in students] + missing_students
    stolaf_non_class_files = list(set(stolaf_files).difference(stolaf_class_files))
    non_stolaf_files = list(set(files).difference(stolaf_files))

    return stolaf_class_files, stolaf_non_class_files, non_stolaf_files


def create_line(file: 'DriveResult', longest_email_len: int, longest_file_name_len: int, longest_link_len: int) -> str:
    if file.create_time is not None:
        create_time = parse(file.create_time).astimezone(tz.gettz('America/Central')).strftime('%x %X %Z')
    else:
        create_time = '---------------------'

    return '{email:<{emailsize}} | {name:<{namesize}} | {link:<{linksize}} | {time}'.format(
        email=file.student_email,
        emailsize=longest_email_len,
        name=file.file_name if file.file_name is not None else 'MISSING',
        namesize=longest_file_name_len,
        link=file.url if file.url is not None else 'MISSING',
        linksize=longest_link_len,
        time=create_time)


def format_file_group(files: List['DriveResult'], title: str):
    longest_email_len = len(max(files,
                                key=lambda f: len(f.student_email) if f.student_email is not None else 0).student_email)
    longest_file_name_len = len(max(files, key=lambda f: len(f.file_name) if f.file_name is not None else 0).file_name)
    longest_link_len = len(max(files, key=lambda f: len(f.url) if f.url is not None else 0).url)

    header = '{email:<{emailsize}} | {name:<{namesize}} | {link:<{linksize}} | {time}'.format(
        email='EMAIL',
        emailsize=longest_email_len,
        name='FILE NAME',
        namesize=longest_file_name_len,
        link='LINK',
        linksize=longest_link_len,
        time='CREATION DATE')

    border = ''.join([
        ''.ljust(longest_email_len + 1, ROW),
        JOIN,
        ''.ljust(longest_file_name_len + 2, ROW),
        JOIN,
        ''.ljust(longest_link_len + 2, ROW),
        JOIN,
        ''.ljust(22, ROW),
    ])

    lines = [title, header, border] + [create_line(file,
                                                   longest_email_len,
                                                   longest_file_name_len,
                                                   longest_link_len)
                                       for file in sorted(files, key=lambda f: f.student_email)]

    return '\n'.join(lines)
