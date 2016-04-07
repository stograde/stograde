# from http://stackoverflow.com/a/2158532/2347774
def flatten(l):
    for el in l:
        if isinstance(el, list) and not isinstance(el, str):
            yield from flatten(el)
        else:
            yield el
