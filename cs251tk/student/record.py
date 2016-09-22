from os import path
from cs251tk.common import chdir
from cs251tk.student.markdownify import markdownify


def record(student, specs, record, basedir, debug):
    recordings = []
    if not record:
        return recordings

    with chdir(student):
        for to_record in record:
            if path.exists(to_record):
                with chdir(to_record):
                    recording = markdownify(to_record, student, specs[to_record], basedir, debug)
            else:
                recording = {
                    'spec': to_record,
                    'student': student,
                    'warnings': {'no submission': True},
                }

            recordings.append(recording)

    return recordings

