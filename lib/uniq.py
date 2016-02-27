# from http://www.peterbe.com/plog/uniqifiers-benchmark


def identity(x):
    return x


def uniq(seq, idfun=identity):
    # order preserving
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = True
        result.append(item)
    return result
