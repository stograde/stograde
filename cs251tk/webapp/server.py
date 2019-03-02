# Adapted from Software Design's serve_my_exe.py program for using
# the SD_app React app.

from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import Popen, PIPE
import sys
import logging

exe_name = ""


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        incoming_data = self.rfile.read(content_length)
        global exe_name
        x = Popen(exe_name, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        (stdout, stderr) = x.communicate(incoming_data)
        outgoing_data = stdout
        if len(stderr) > 0:
            logging.debug(stderr, file=sys.stderr)
        self._set_headers()
        self.wfile.write(outgoing_data)

    def log_message(self, format, *args):
        return


def run_server(server=HTTPServer, handler=S, port=25100):
    server_address = ('', port)
    httpd = server(server_address, handler)
    logging.debug('Starting httpd...')
    httpd.serve_forever()
