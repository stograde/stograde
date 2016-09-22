from .emailify import emailify
from .send_email import send_email


def send_recordings(recordings, name, to, debug):
    email = emailify(recordings, name, to, debug)
    send_email(email)
