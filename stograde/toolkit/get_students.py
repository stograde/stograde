import logging
import re
from typing import Dict, Any, List

from stograde.common import flatten


def clean_header(text):
    return text.strip('[]')


def get_students(args: Dict[str, Any]) -> List[str]:
    """Get students from the command line or the students.txt file.
    Passing any students on the command line will ignore the file contents"""
    sections = args['sections']
    cmd_line_students = args['students']

    students = [student for group in cmd_line_students for student in group]
    if not students:
        file_students = get_students_from_file()

        if sections:
            file_students = filter_sections(file_students, sections)

        students = list(flatten([file_students[section] for section in file_students]))

    return sorted(set(students))


def get_students_from_file():
    """Get students from a students.txt file"""
    try:
        with open('students.txt', 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        lines = []

    # Make a list of all lines in the file
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]

    # Make a list of all the section headers in the file
    # Include a 'no_section' group for any students listed before the sections,
    # or if there are no sections
    group_regex = re.compile(r'\[.*\]')
    group_list = ['no_section'] + [clean_header(line) for line in lines if group_regex.match(line)]

    # Go through each line, adding students to section lists
    # When a section header is reached, switch to that section's list
    # for all students until the next section header
    groups = {group: [] for group in group_list}
    current_group = group_list[0]  # Start with 'no_section' section
    for line in lines:
        if group_regex.match(line):
            current_group = clean_header(line)  # line is a section header
        else:
            groups[current_group].append(line)  # line is a student

    return groups


def filter_sections(section_lists: Dict[str, List[str]], sections: List[str]) -> Dict[str, List[str]]:
    """Get only the desired sections"""
    filtered_sections = {}
    for section_name in sections:
        student_set = []
        prefixed = 'section-{}'.format(section_name)

        if section_name in section_lists:
            student_set = section_lists[section_name]
        elif prefixed in section_lists:
            student_set = section_lists[prefixed]
        else:
            logging.warning('Neither section [section-{0}] nor [{0}] could be found in ./students.txt'
                            .format(section_name))

        filtered_sections[section_name] = student_set

    return filtered_sections
