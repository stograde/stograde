import smtplib


def send_email(msg):
    # Send the message via our own SMTP server.
    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)
