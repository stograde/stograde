"""
Adapted from bridge.py from the SD course.

Simple HTTP server in python, that invokes an executable to handle requests.
Send a POST request::
    curl -d "3ok" http://localhost:25199
"""
import logging
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import *
from ..common import chdir

exe_name = "a.out"
work_dir = "."
exe_mtime = -1
message_id = {}
yaml_files_name = "app.files"
mem_file_name = "app.mem"
yaml_mtime = -1
separator = '\n---\n'


def has_top_key(key, yaml):
    return yaml.startswith(key) or -1 != yaml.find('\n' + key)


def get_top_key(key, yaml):
    if yaml.startswith(key):
        res = yaml[len(key):]
    else:
        pos = yaml.find('\n' + key)
        if -1 == pos:
            return False
        res = yaml[pos + len(key) + 1:]
    # trim off after newline
    pos2 = res.find('\n')
    if -1 == pos2:
        return res
    res = res[:pos2]
    return res


def load_binary(filename):
    with open(filename, 'rb') as fh:
        return fh.read()


class S(BaseHTTPRequestHandler):
    def _set_headers(self, content):
        self.send_response(200)
        self.send_header('Content-type', content)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def use_exe(self, first_name, yaml_part, incoming_data):
        global exe_name, exe_mtime, message_id, separator
        new_mtime = os.path.getmtime(exe_name)
        is_poll = False
        just_recompiled = False
        if new_mtime > exe_mtime:  # restart!
            message_id[first_name] = 0
            incoming_data = "- message_id: " + str(message_id[first_name]) + "\n"
            incoming_data += "- first_name: " + first_name + separator
            incoming_data = incoming_data.encode()
            logging.debug("recompiled")
            just_recompiled = True
        else:
            if has_top_key('- initialize: ', yaml_part):  # initialization
                message_id[first_name] = 0
                incoming_data = "- message_id: " + str(message_id[first_name]) + "\n"
                incoming_data += "- first_name: " + first_name + separator
                incoming_data = incoming_data.encode()
                logging.debug('init_client')
            elif has_top_key('- event_info:', yaml_part):  # user interaction
                message_id[first_name] += 1
                incoming_data = ("- message_id: " + str(message_id[first_name]) + "\n").encode() + incoming_data
                logging.debug('event')
            else:  # just a poll
                # is_poll = True
                incoming_data = ("- message_id: " + str(message_id[first_name]) + " poll\n").encode() + incoming_data
        if is_poll:
            outgoing_data = 'same_exe'
            outgoing_data = bytes(outgoing_data, "utf-8")
        else:
            vverbose = False
            if vverbose:
                logging.debug(" running with incoming len:\n")
                sys.stderr.buffer.write(incoming_data)
                logging.debug("\n")
            try:
                proc = Popen(os.path.join(os.getcwd(), exe_name), stdin=PIPE, stdout=PIPE, stderr=PIPE)
                try:
                    (stdout_, stderr_) = proc.communicate(incoming_data, timeout=2)
                except TimeoutExpired:
                    proc.kill()
                    (stdout_, stderr_) = proc.communicate()
                    stderr_ = b'timeout expired:  your code may have an infinite loop!\n' + stderr_
            except FileNotFoundError:
                stdout_ = ""
                stderr_ = "File {} not found".format(os.path.join(os.getcwd(), exe_name))
            if 'str' == type(stdout_):
                stdout_ = bytes(stdout_, 'utf-8')
                stderr_ = bytes(stderr_, 'utf-8')
            if vverbose:
                logging.debug("\n STDOUT ")
                sys.stderr.buffer.write(stdout_)
                logging.debug("\n")
            keyword = b'React Native'
            if stdout_.startswith(keyword):
                if vverbose:
                    logging.debug(" keyword ")
                stdout_ = stdout_[len(keyword):]
            elif b'same_exe' == stdout_:
                if vverbose:
                    logging.debug(" was_poll ")
            elif b'timeout' == stdout_:
                if vverbose:
                    logging.debug(" timeout ")
            else:
                if vverbose:
                    logging.debug(" no_keyword ")
                if vverbose:
                    sys.stderr.buffer.write(stdout_)
                if os.path.isfile(yaml_files_name):
                    if just_recompiled:
                        logging.debug(" sending static ")
                    stdout_ = self.use_static_yaml_inner()
                else:
                    stdout_ = b''
            outgoing_data = stdout_
            if len(stderr_) > 0:
                outgoing_data = b'- stderr: ' + stderr_ + bytes(chr(0), "utf-8") + outgoing_data
        self._set_headers('text/html')
        self.wfile.write(outgoing_data)
        exe_mtime = new_mtime

    def use_static_yaml_inner(self):
        global separator, yaml_mtime
        new_mtime = os.path.getmtime(yaml_files_name)
        new_mtime2 = os.path.getmtime(mem_file_name)
        if new_mtime2 > new_mtime:
            new_mtime = new_mtime2
        if new_mtime > yaml_mtime:
            logging.debug("sending static yaml")
        outgoing_data = ''
        with open(yaml_files_name, 'r') as fh:
            for line in fh:
                line = line.lstrip()
                if line[0] != '#':
                    line = line.rstrip()
                    with open(line, 'r') as fh2:
                        outgoing_data += '\n' + fh2.read()
            outgoing_data += separator
            mem_data = b''
            with open(mem_file_name, 'rb') as fh3:
                mem_data += fh3.read()
            while len(mem_data) < 10000:  # fill in the rest with null bytes
                mem_data += b'\0'
            outgoing_data = outgoing_data.encode('utf8') + mem_data
            # print('outgoing_data is as follows:\n', outgoing_data)
            yaml_mtime = new_mtime
        return outgoing_data

    def use_static_yaml(self):
        outgoing_data = self.use_static_yaml_inner()
        self._set_headers('text/html')
        self.wfile.write(outgoing_data)

    def do_GET(self):
        if self.path.endswith(".png"):
            self._set_headers('image/png')
            self.wfile.write(load_binary(self.path[self.path.rfind("/") + 1:]))

    def do_POST(self):
        with chdir(work_dir):
            content_length = int(self.headers['Content-Length'])
            incoming_data = self.rfile.read(content_length)
            # parse the incoming data, to look for some key parts
            global exe_name, separator
            sep_pos = incoming_data.find(separator.encode())
            if -1 == sep_pos:
                yaml_part = ''
            else:
                yaml_part = incoming_data[:sep_pos].decode() + '\n'
            first_name = get_top_key('- first_name: ', yaml_part)

            # does the executable exist?
            if os.path.isfile(exe_name):
                logging.debug(" has_exe ")
                self.use_exe(first_name, yaml_part, incoming_data)
            elif os.path.isfile(yaml_files_name):
                logging.debug(" no_exe ")
                self.use_static_yaml()
            else:
                logging.debug(" nothing ")

    def log_message(self, format, *args):
        pass


def run_server(server_class=HTTPServer, handler_class=S, port=25199):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
