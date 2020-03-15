def truncate(string: str, length: int, encoding='utf-8') -> str:
    encoded = string.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')
