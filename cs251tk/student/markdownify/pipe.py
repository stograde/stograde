from glob import glob
import shlex

from cs251tk.common import flatten
from cs251tk.common import run


def expand_chunk(command_chunk):
    """Take a chunk of a command and expand it, like a shell"""
    if '*' in command_chunk:
        return glob(command_chunk)
    return [command_chunk]


def process_chunk(command):
    """Takes one piece of a pipeline and formats it for run_command"""
    # decode('unicode_escape') de-escapes the backslash-escaped strings.
    # like, it turns the \n from "echo Hawken \n 26" into an actual newline,
    # like a shell would.
    cmd = bytes(command, 'utf-8').decode('unicode_escape')

    # shlex splits commands up like a shell does.
    # I'm not entirely sure how it differs from just split(' '),
    # but figured it wasn't a bad thing to use.
    cmds = shlex.split(cmd)

    return list(flatten([expand_chunk(c) for c in cmds]))


def pipe(cmd_string):
    cmds = cmd_string.split(' | ')

    input_for_cmd = None
    for cmd in cmds[:-1]:
        _, input_for_cmd, _ = run(process_chunk(cmd), input_data=input_for_cmd)
        input_for_cmd = input_for_cmd.encode('utf-8')

    final_cmd = process_chunk(cmds[-1])
    return final_cmd, input_for_cmd
