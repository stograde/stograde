import re


def determine_assignment_type(string):
    if string in ['hw', 'homework', 'homeworks']:
        return 'hw'
    if string in ['lab']:
        return 'lab'
    return None


def parse_commit_msg_for_assignments(message):
    matches = [m.groups() for m in re.finditer(r'([a-z]+) ?(\d+)', message.lower())]
    results = [(determine_assignment_type(kind), num) for kind, num in matches]

    return [pair for pair in results if pair[0] is not None]
