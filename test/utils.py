import re

from stograde.common import run
from stograde.toolkit.progress_bar import CHAR


def git(cmd, *args):
    return run(['git', cmd, *args])


def touch(file):
    return run(['touch', file])


def check_e2e_err_output(err: str):
    return re.compile(r"Could not get URL from data directory: "
                      r"Command '\['.*\]' returned non-zero exit status 1\.\r?\n"
                      r"Defaulting to SD\r?\n"
                      r"\r\[ {6}\] .*, .*, .*, .*, .*, .*"
                      rf"\r\[{re.escape(CHAR)} {{5}}\] .*, .*, .*, .*, .*"
                      rf"\r\[{re.escape(CHAR)}{{2}} {{4}}\] .*, .*, .*, .*"
                      rf"\r\[{re.escape(CHAR)}{{3}} {{3}}\] .*, .*, .*"
                      rf"\r\[{re.escape(CHAR)}{{4}} {{2}}\] .*, .*"
                      rf"\r\[{re.escape(CHAR)}{{5}} \] .*"
                      rf"\r\[{re.escape(CHAR)}{{6}}\] *").match(err)
