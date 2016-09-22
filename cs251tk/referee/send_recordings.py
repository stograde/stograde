from .emailify import emailify
from .send_email import send_email


def send_recordings(recordings, name, to, debug):
    print(name, to)
    email = emailify(recordings, name, to, debug)
    print(email)
    send_email(email)
