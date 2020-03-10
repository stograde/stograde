import logging
import re

LAB_REGEX = re.compile(r'^LAB', re.IGNORECASE)


def ci_analyze(records):
    passing = True
    for record in records:
        try:
            for filename, file in record['files'].items():
                # Alert student about any missing files
                if file['missing'] and not file['optional']:
                    logging.error("{}: File {} missing".format(record['spec'], file['filename']))
                    if not re.match(LAB_REGEX, record['spec']):
                        passing = False
                else:
                    # Alert student about any compilation errors
                    for compilation in file['compilation']:
                        if compilation['status'] != 'success':
                            if file['optional_compile']:
                                logging.warning("{}: File {} compile error (This did not fail the build)"
                                                .format(record['spec'], file['filename']))
                            else:
                                logging.error("{}: File {} compile error:\n\n\t{}"
                                              .format(record['spec'], file['filename'],
                                                      compilation['output'].replace("\n", "\n\t")))
                                if not re.match(LAB_REGEX, record['spec']):
                                    passing = False
        except KeyError:
            logging.error("KeyError with {}".format(record['spec']))
    return passing
