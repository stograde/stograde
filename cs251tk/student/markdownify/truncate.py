def truncate(string, length, encoding='utf-8'):
    encoded = string.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')
