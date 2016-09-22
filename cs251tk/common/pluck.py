def pluck(lst, attr):
    """Build a list of the values of the given attribute from the source list"""
    return [it[attr] for it in lst]
