import smtplib


def send_email(msg):
    # Send the message via our own SMTP server.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
        s.send_message(msg)
