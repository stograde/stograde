import logging


def ci_analyze(records):
    passing = True
    for record in records:
        try:
            for file in record['files']:
                # Alert student about any missing files
                if file['missing'] and not record['files'][file]['optional']:
                    logging.error("{}: File {} missing".format(record['spec'], record['files'][file]['filename']))
                    passing = False
                else:
                    # Alert student about any compilation errors
                    for compilation in record['files'][file]['compilation']:
                        if compilation['status'] != 'success':
                            logging.error("{}: File {} compile error:\n\n\t{}"
                                          .format(record['spec'], record['files'][file]['filename'],
                                                  compilation['output'].replace("\n", "\n\t")))
                            passing = False
        except KeyError:
            logging.error("KeyError with {}".format(record['spec']))
    return passing
