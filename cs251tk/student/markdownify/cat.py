def cat(filename):
    """Return the contents of a file. Replaces the `cat` command.

    This function took about ~148 time units per call, while
    run(['cat']) needed ~4688 time units.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as infile:
            return 'success', infile.read()
    except Exception:
        return 'failure', None
