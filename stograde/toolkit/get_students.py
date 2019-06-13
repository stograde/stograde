import re


def clean_header(text):
    return text.strip('[]')


def get_students():
    try:
        with open('students.txt', 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        lines = []

    lines = [l.strip() for l in lines]
    lines = [l for l in lines if l]
    group_regex = re.compile(r'\[.*\]')
    group_list = [clean_header(l) for l in lines if group_regex.match(l)]
    if not group_list:
        group_list = ['my']

    groups = {group: [] for group in group_list}
    current_group = group_list[0]
    for line in lines:
        if group_regex.match(line):
            current_group = clean_header(line)
        else:
            groups[current_group].append(line)

    return groups
