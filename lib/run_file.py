#!/usr/bin/env python3

import sys
import os
from .run_command import run


def run_file(filePath, input='', **kwargs):
    return run([filePath], input=input, timeout=4, **kwargs)


if __name__ == '__main__':
    filePath = sys.argv[1]
    print(run_file(filePath))