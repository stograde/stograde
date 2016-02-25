def add_newline_before(seq, lines):
    new_lines = []
    for line in lines:
        if line and line[0:len(seq)] == seq:
            new_lines.append('\n' + line)
        else:
            new_lines.append(line)

    return ''.join(new_lines)
