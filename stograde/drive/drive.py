import datetime
from dateutil import tz
from dateutil.parser import parse
import os
import re
import sys
from typing import Any, Dict, List, Tuple, Optional, Union, Set

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .drive_result import DriveResult
from ..formatters.tabulate import JOIN, ROW
from ..process_assignment.assignment_type import AssignmentType, get_assignment_number, get_assignment_type


def authenticate_drive() -> Credentials:
    """Authenticate the connection"""
    if not os.path.exists('client_secret.json'):
        print('client_secret.json is required for stograde drive functionality.', file=sys.stderr)
        print('Follow the steps at https://github.com/stograde/stograde/blob/main/docs/DRIVE.md '
              'to create the file.', file=sys.stderr)
        print('If you have already created it, please make sure it is located in the directory where you are '
              'running stograde.', file=sys.stderr)
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json',
                                                     'https://www.googleapis.com/auth/drive.metadata.readonly')
    return flow.run_console()


def request_files(service,
                  next_page_token: Optional[str],
                  email: str,
                  date: datetime.date) -> Tuple[List[Dict[str, Union[str, List[Dict[str, Any]]]]],
                                                Optional[str]]:
    """Get metadata about 100 files at a time.
    Returns a list of file metadata and the nextPageToken if it exists.
    If nextPageToken does not exist, then we have reached the end of the list"""
    response = service.files().list(q="modifiedTime > '{year}-{month}-01T00:00:00' and "
                                      "('{email}' in writers or '{email}' in readers)"
                                    .format(year=date.year,
                                            month='01' if date.month < 7 else '07',
                                            email=email),
                                    pageSize=100,
                                    fields='files(createdTime,name,owners,permissions,webViewLink),nextPageToken',
                                    pageToken=next_page_token).execute()

    return [file for file in response['files']], response.get('nextPageToken', None)


def get_all_files(credentials: Credentials, email: str) -> Set['DriveResult']:
    """Get all files shared with the specified email in the current half-year
    (January-June or July-December of the current year)"""
    # Create drive service with provided credentials
    service = build('drive', 'v3', credentials=credentials, cache_discovery=False)

    all_user_files = []

    next_page_token = None
    date = datetime.date.today()

    while True:
        # Request the next page of files
        metadata, next_page_token = request_files(service, next_page_token, email, date)
        all_user_files = all_user_files + metadata

        print('\r{} files processed'.format(len(all_user_files)), end='')

        # If we have reached the end of the list of documents, next_page_token will be None
        if next_page_token is None:
            break

    return {DriveResult(student_email=file['owners'][0]['emailAddress'],
                        file_name=file['name'],
                        create_time=file['createdTime'],
                        url=file['webViewLink'])
            for file in all_user_files}


def get_assignment_files(assignment: str,
                         credentials: Credentials,
                         email: str,
                         regex: Optional[str]) -> Set['DriveResult']:
    """Filter out only files that contain the name of the assignment in their name"""
    if regex:
        try:
            re.compile(str(regex))
            reg = regex
        except re.error as err:
            print('Invalid regex: {}'.format(err), file=sys.stderr)
            sys.exit(1)
    else:
        try:
            a_type = get_assignment_type(assignment)
            a_num = get_assignment_number(assignment)
            if a_type is AssignmentType.DAY:
                type_reg = 'day'
            elif a_type is AssignmentType.HOMEWORK:
                type_reg = '(hw|homework)'
            elif a_type is AssignmentType.LAB:
                type_reg = 'lab'
            elif a_type is AssignmentType.WORKSHEET:
                type_reg = '(ws|worksheet)'
        except ValueError:
            print('Could not parse assignment name {}'.format(assignment), file=sys.stderr)
            sys.exit(1)

        # noinspection PyUnboundLocalVariable
        reg = '.*' + type_reg + ' *0*' + str(a_num) + r'(\D.*|$)'

    files = get_all_files(credentials=credentials, email=email)

    return set(filter(lambda f: re.match(reg, f.file_name, re.IGNORECASE) is not None, files))


def group_files(files: Set['DriveResult'],
                students: List[str]) -> Tuple[Set['DriveResult'],
                                              Set['DriveResult'],
                                              Set['DriveResult']]:
    """Group files found into three groups:
        - Students whose username is in the students.txt file
        - Students whose username is not in the students.txt file
        - Students who shared the file using an email that does not end with @stolaf.edu

    If a file is not found for a student in the students.txt file, a placeholder result is added to the
    first group."""
    # Create placeholders for students who are listed in the students.txt file
    # that have not shared a document using their school email
    missing_students = {DriveResult(student + '@stolaf.edu', 'MISSING', None, 'MISSING') for student in
                        list(set(students).difference({file.student_email[:-11] for file in files}))}

    # Get all documents that were shared by stolaf.edu emails
    stolaf_files = {file for file in files if file.student_email.endswith('@stolaf.edu')}

    # Get all documents that were shared by students listed in the students.txt file
    stolaf_class_files = {file for file in files if file.student_email[:-11] in students} | missing_students

    # Get all documents that were shared by students not listed in the students.txt file
    stolaf_non_class_files = stolaf_files.difference(stolaf_class_files)

    # Get any documents shared with non-stolaf.edu emails
    non_stolaf_files = files.difference(stolaf_files)

    return stolaf_class_files, stolaf_non_class_files, non_stolaf_files


def create_line(file: 'DriveResult', longest_email_len: int, longest_file_name_len: int, longest_link_len: int) -> str:
    """Create a line of the table"""
    if file.create_time is not None:
        # 'CST6CDT,M3.2.0,M11.1.0' represents CST/CDT
        create_time = parse(file.create_time).astimezone(tz.gettz('CST6CDT,M3.2.0,M11.1.0')).strftime('%x %X %Z')
    else:
        create_time = ''.ljust(21, '-')

    return '{email:<{emailsize}} | {name:<{namesize}} | {link:<{linksize}} | {time}'.format(
        email=file.student_email,
        emailsize=longest_email_len,
        name=file.file_name,
        namesize=longest_file_name_len,
        link=file.url,
        linksize=longest_link_len,
        time=create_time)


def format_file_group(files: Set['DriveResult'], title: str):
    """Create a table for a group of documents (see group_files for groupings)"""
    # Determine longest length for each column
    longest_email_len = len(max(files,
                                key=lambda f: len(f.student_email) if f.student_email is not None else 0).student_email)
    longest_file_name_len = len(max(files, key=lambda f: len(f.file_name) if f.file_name is not None else 0).file_name)
    longest_link_len = len(max(files, key=lambda f: len(f.url) if f.url is not None else 0).url)

    # Create the header row
    header = '{email:<{emailsize}} | {name:<{namesize}} | {link:<{linksize}} | {time}'.format(
        email='EMAIL',
        emailsize=longest_email_len,
        name='FILE NAME',
        namesize=longest_file_name_len,
        link='LINK',
        linksize=longest_link_len,
        time='CREATION DATE')

    # Create the border between the header row and the rest of the table
    border = ''.join([
        ''.ljust(longest_email_len + 1, ROW),
        JOIN,
        ''.ljust(longest_file_name_len + 2, ROW),
        JOIN,
        ''.ljust(longest_link_len + 2, ROW),
        JOIN,
        ''.ljust(22, ROW),
    ])

    # Create and return the table
    lines = [title, header, border] + [create_line(file,
                                                   longest_email_len,
                                                   longest_file_name_len,
                                                   longest_link_len)
                                       for file in sorted(files, key=lambda f: f.student_email)]

    return '\n'.join(lines)
