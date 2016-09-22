from textwrap import dedent, indent
from .markdown import format_files_list, format_warning
from email.mime.text import MIMEText
import traceback

GITHUB_MARKDOWN = False


def format_collected_data(data, to):
    body = markdown(data)
    msg = MIMEText(body)
    msg['To'] = to
    msg['From'] = 'cs251-tas@stolaf.edu'
    msg['Subject'] = build_subject(data)
    return


def body(data):
    files = format_files_list(data.get('files', {}))
    warnings = [format_warning(warning, value) for warning, value in data['warnings'].items()]
    warnings = [w for w in warnings if w]

    header = '# {spec} – {student}\n'.format_map(data)

    if warnings:
        header += '\n' + '\n'.join(warnings) + '\n'

    if files:
        files = '\n\n' + files

    return dedent(header + files)



def build_subject(data):

