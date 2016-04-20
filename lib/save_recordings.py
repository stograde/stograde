from .format_collected_data import format_collected_data
from .helpers import warn


def record_recording(results, output_file):
    str_results = format_collected_data(results)
    # str_results = '---\n' + yaml.dump(results)
    try:
        output_file.write(str_results)
    except Exception as err:
        warn('error! could not write recording:', err)


def save_recordings(records, files):
    for name, recording_content in records.items():
        if name in files:
            record_recording(recording_content, files[name])
