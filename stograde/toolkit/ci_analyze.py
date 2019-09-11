import logging


def ci_analyze(records):
    passing = True
    for record in records:
        try:
            for filename in record['files']:
                file = record['files'][filename]
                # Alert student about any missing files
                if file['missing'] and not file['optional']:
                    logging.error("{}: File {} missing".format(record['spec'], file['filename']))
                    passing = False
                else:
                    # Alert student about any compilation errors
                    for compilation in file['compilation']:
                        if compilation['status'] != 'success':
                            message = "{}: File {} compile error:\n\n\t{}" \
                                .format(record['spec'], file['filename'],
                                        compilation['output'].replace("\n", "\n\t"))
                            if file['optional_compile']:
                                logging.warning(message)
                            else:
                                logging.error(message)
                                passing = False
        except KeyError:
            logging.error("KeyError with {}".format(record['spec']))
    return passing
