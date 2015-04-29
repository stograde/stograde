#!/usr/bin/env python3

from sys import argv, stdin


def add_newline_before(seq, lines):
    new_lines = []
    for line in lines:
        if line and line[0:len(seq)] == seq:
            new_lines.append('\n' + line)
        else:
            new_lines.append(line)

    return ''.join(new_lines)


if __name__ == '__main__':
    print(add_newline_before(argv[1], stdin.readlines()))
