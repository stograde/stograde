# from http://stackoverflow.com/a/2158532/2347774
def flatten(lst):
    """Flatten a list"""
    for elem in lst:
        if isinstance(elem, list) and not isinstance(elem, str):
            yield from flatten(elem)
        else:
            yield elem
