from cs251tk.formatters import format_collected_data, markdown
from email.mime.text import MIMEText


def emailify(recordings, name, to, debug):
    results = format_collected_data(recordings,
                                    group_by='student',
                                    formatter=markdown,
                                    debug=debug)

    body = '\n'.join([r['content'] for r in results])
    msg = MIMEText(body)
    msg['To'] = '{} <{}>'.format(name, to)
    msg['From'] = 'cs251-tas@stolaf.edu'
    msg['Subject'] = build_subject(results)
    return msg


def build_subject(results):
    return 'The ' + ', '.join([r['assignment'] for r in results]) + ' submission'
