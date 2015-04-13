#!/usr/bin/env python3

import sys, os
from .run_command import run

def run_file(filePath, input=''):
  return run([filePath], input=input, timeout=4)


if __name__ == '__main__':
  filePath = sys.argv[1]
  print(run_file(filePath))
