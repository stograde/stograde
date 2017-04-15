from cs251tk.formatters import format_collected_data, html, markdown
from cs251tk.common import group_by
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def emailify(recordings, name, to, debug):
    fancy = format_collected_data(recordings,
                                  group_by='student',
                                  formatter=html,
                                  debug=debug)

    plaintext = format_collected_data(recordings,
                                      group_by='student',
                                      formatter=markdown,
                                      debug=debug)

    grouped = dict(group_by(recordings, lambda s: s['student']))

    print(plaintext)
    print(grouped)

    # `grouped` is a dictionary, from username to list of assignment results
    if not recordings:
        raise Exception('No students found to create an email!')

    fancy_body = '\n'.join([r['content'] for r in list(fancy.values())[0]])
    plaintext_body = '\n'.join([r['content'] for r in list(plaintext.values())[0]])
    print(fancy_body)
    print(plaintext_body)

    msg = MIMEMultipart('alternative')
    msg['To'] = '{} <{}>'.format(name, to)
    msg['From'] = 'cs251-tas@stolaf.edu'
    msg['Subject'] = build_subject(list(fancy.values())[0])

    msg.attach(MIMEText(plaintext_body, 'plain'))
    msg.attach(MIMEText(fancy_body, 'html'))

    return msg


def build_subject(results):
    return '[referee] Results for ' + ', '.join([r['assignment'] for r in results]) + ' submission'
