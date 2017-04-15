from cs251tk.formatters import format_collected_data, markdown
from email.mime.text import MIMEText


def emailify(recordings, name, to, debug):
    grouped = format_collected_data(recordings,
                                    group_by='student',
                                    formatter=markdown,
                                    debug=debug)

    # `grouped` is a dictionary, from username to list of assignment results
    if not grouped:
        raise Exception('No students found to create an email!')
    if len(grouped) > 1:
        raise Exception('More than one student found when creating an email!')
    assignments = list(grouped.values())[0]

    body = '\n'.join([r['content'] for r in assignments])
    msg = MIMEText(body)
    msg['To'] = '{} <{}>'.format(name, to)
    msg['From'] = 'cs251-tas@stolaf.edu'
    msg['Subject'] = build_subject(assignments)
    return msg


def build_subject(results):
    return 'The ' + ', '.join([r['assignment'] for r in results]) + ' submission'
