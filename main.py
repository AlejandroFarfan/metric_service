#!/usr/bin/env python

"""
Usage::
    ./main.py [<port>]
Send a GET request::
    curl http://localhost/log
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""

import gzip
import io
import json

import binascii

from http.server import BaseHTTPRequestHandler, HTTPServer
from data_keeper import data_keeper

post_count = 0
request_array = []


def get_dic_array(event_dic):
    events_array = []
    for i in range(len(event_dic)):
        events_array.append(event_dic[i])
    return events_array


# noinspection PyPep8Naming
class S(BaseHTTPRequestHandler):
    Max_Size = 5
    data = data_keeper()

    def _set_headers(self, status_code=200):  # OK
        self.send_response(status_code)
        #        self.send_response(401)  # unauthorized
        #        self.send_response(403)  # forbidden
        #        self.send_response(404)  # not found

        #        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Type', 'application/json')

        self.end_headers()

    def do_GET(self):
        self._set_headers()
        request_path = self.path
        self.wfile.write(b"{}")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        global post_count
        global request_array

        request_path = self.path

        request_headers = self.headers
        content_length = request_headers.get('content-length')
        length = int(content_length) if content_length else 0

        print(request_headers)
        # print(binascii.hexlify((self.rfile.read(length))))

        request_content = ""

        if request_headers.get('Content-Encoding') == 'gzip':
            f_in = io.BytesIO()
            f_in.write(self.rfile.read(length))
            f_in.seek(0)

            with gzip.GzipFile(fileobj=f_in, mode='rb') as fo:
                print(fo.read().decode())
                request_content = fo.read().decode()

        else:
            # print(self.rfile.read(length))
            request_content = self.rfile.read(length)

        print("<----- Request End -----\n")


        if request_path.startswith("/log/"):
            print("<----- Add LOG -----\n")
            print(request_content)
            events_data = json.loads(request_content)
            test = events_data["log"]
            request_array.append(test)
            self.data.feed_data(test)

            print(request_array)
            self._set_headers(200)
            self.wfile.write('Log received'.encode('ascii'))


        self._set_headers()




def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    try:
        if len(argv) == 2:
            run(port=int(argv[1]))
        else:
            run()

    except KeyboardInterrupt:
        pass
