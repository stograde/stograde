import smtplib
import os


def send_email(msg):
    username = os.getenv('STOGRADE_EMAIL_USERNAME', os.getenv('CS251TK_EMAIL_USERNAME', None))
    if not username:
        raise Exception('Missing $STOGRADE_EMAIL_USERNAME')

    password = os.getenv('STOGRADE_EMAIL_PASSWORD', os.getenv('CS251TK_EMAIL_PASSWORD', None))
    if not password:
        raise Exception('Missing $STOGRADE_EMAIL_PASSWORD')

    # Send the message via our own SMTP server.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
        s.login(username, password)
        s.send_message(msg)
