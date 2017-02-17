def get_filenames(spec):
    """returns the list of files from an assignment spec"""
    return [file['filename'] for file in spec['files']]
