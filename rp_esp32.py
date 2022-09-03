
# Simple Python ESP32 WiFi interface
# Runs under pimoroni-pico-v0.2.6-micropython-v1.16.uf2
# See https://github.com/pimoroni/pimoroni-pico/releases/tag/v0.2.6
#
# For detailed description, see https://iosoft.blog
#
# Copyright (c) 2021 Jeremy P Bentham
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# v0.06 JPB 26/9/21  Tidied up for release
# v0.07 JPB 19/10/21 Added content-type to put_http_text
# v0.08 JPB 23/10/21 Changed recv_length to use avail_data (was avail_server) 

import os, utime, picowireless, machine
from micropython import const

WIFI_SSID = "testnet"
WIFI_PASS = "testpass"

ADC_PINS = 26, 27, 28
ADC_SCALE = 3.3 / 65536
TCP_MODE = const(0)
HTTP_PORT = const(80)
MAX_SPI_DLEN = const(128)

DIRECTORY     = "/"
TEST_FNAME    = "test.html"
INDEX_FNAME   = "index.html"
DATA_FNAME    = "data.csv"
CAPTURE_FNAME = "capture.csv"
ICON_FNAME    = "favicon.ico"

HTTP_OK = "HTTP/1.1 200 OK\r\n"
CONTENT_LEN = "Content-Length: %u\r\n"
CONTENT_TYPE = "Content-type %s\r\n"
TEST_PAGE = '''<!DOCTYPE html><html>
    <head><style>table, th, td {border: 1px solid black; margin: 5px;}</style></head>
    <body><h2>Pi Pico web server</h2>%s</body></html>'''
NOT_FOUND = 'HTTP/1.1 404 Not found\r\nContent-Length: 14\r\n\r\nFile not found'
DISABLE_CACHE = "Cache-Control: no-cache, no-store, must-revalidate\r\n"
DISABLE_CACHE += "Pragma: no-cache\r\nExpires: 0\r\n"
HEAD_END = "\r\n"

# MicroPython WiFi functions: see pimoroni-pico-0.2.6/drivers/esp32spi/esp32spi.cpp
# Matching MicroPython functions: nina-fw/main/CommandHandler.cpp

# Wifi status (firmware getConnStatus): see nina-fw/arduino/libraries/WiFi/src/Wifi.h
status_strs = {0:"idle", 1:"connecting", 2:"scan complete", 3:"connected", 4:"connect failed",
               5:"connection lost", 6:"disconnected", 255:"no WiFi"}
STATUS_OK, STATUS_FAIL = 3, 4

# Check elapsed msec for timeout
def mstimeout(start, tout):
    return utime.ticks_ms()-start > tout

# Class for ESP32 WiFi interface
class ESP32:
    def __init__(self):
        self.last_status = self.server_sock = None
        self.txcount = 0
        picowireless.init()
        picowireless.set_power_mode(0)

    # Return status of WiFi connection
    def get_wifi_status(self):
        return picowireless.get_connection_status()

    # Return status of socket connection
    def get_server_status(self):
        return False if self.server_sock is None else picowireless.get_server_state(self.server_sock)

    # Get my IP address
    def get_ip_address(self):
        return picowireless.get_ip_address()

    # Display status of WiFi connection
    def disp_wifi_status(self, status):
        s = status_strs[status] if status in status_strs else str(status)
        print("WiFi status: %s" % s)

    # Check WiFi status, display a change
    def check_wifi_status(self):
        status = self.get_wifi_status()
        if status != self.last_status:
            self.disp_wifi_status(status)
            self.last_status = status
        return status

    # Connect to WiFi network, given SSID and password
    def connect(self, ssid, passwd):
        picowireless.wifi_set_passphrase(ssid, passwd)

    # Get client socket, given server socket
    def get_client_sock(self, server_sock):
        return picowireless.avail_server(server_sock)

    # Start TCP server, given port number
    def start_server(self, port):
        self.server_sock = picowireless.get_socket()
        picowireless.server_start(port, self.server_sock, 0)

    # Return length of data received by server
    def recv_length(self, sock):
        return picowireless.avail_data(sock)
        #return picowireless.avail_server(sock)

    # Return data received by server
    def recv_data(self, sock):
        return picowireless.get_data_buf(sock)

    # Send block of data to client
    def send_data(self, sock, data, tout=1000):
        picowireless.send_data(sock, data)
        startime = utime.ticks_ms()
        while not picowireless.check_data_sent(sock):
            if mstimeout(startime, tout):
                print("Client Tx timeout")
                self.send_end(sock)
                return False
        return True

    # Mark end of data sent to client
    def send_end(self, sock):
        picowireless.client_stop(sock)

    # Get HTTP request from client
    def get_http_request(self):
        self.client_sock = self.get_client_sock(self.server_sock)
        request = ""
        client_dlen = self.recv_length(self.client_sock)
        while self.client_sock != 255 and client_dlen > 0:
            print("Client socket %d len %d: " % (self.client_sock, client_dlen), end="")
            req = self.recv_data(self.client_sock)
            if req:
                request += req.decode("utf-8")
            client_dlen = self.recv_length(self.client_sock)
        return request

    def get_http_request2(self, mstout=1000):
        self.client_sock = self.get_client_sock(self.server_sock)
        client_dlen = self.recv_length(self.client_sock)
        if self.client_sock != 255 and client_dlen > 0:
            print("len %u" % client_dlen)
            startime = utime.ticks_ms()
            print("Client socket %d len %d: " % (self.client_sock, client_dlen), end="")
            req = b""
            while len(req) < client_dlen:
                req += self.recv_data(self.client_sock)
                if utime.ticks_ms() - startime > mstout:
                    print("Client Rx timeout")
                    self.send_end(self.client_sock)
                    return None
            request = req.decode("utf-8")
            return request
        return None

    # Split data into blocks, send to client
    def put_data(self, data):
        n = 0
        while n < len(data):
            d = data[n: n+MAX_SPI_DLEN]
            self.send_data(self.client_sock, d)
            n += len(d)

    # Send 'not found' error to client
    def put_http_404(self):
        self.send_data(self.client_sock, NOT_FOUND)
        self.send_end(self.client_sock)

    # Send text response to client
    def put_http_text(self, text, content="text/html", hdr=""):
        resp = HTTP_OK + CONTENT_LEN%len(text)
        resp += CONTENT_TYPE%content + hdr + HEAD_END
        self.put_data(resp)
        self.put_data(text)
        self.send_end(self.client_sock)
        self.txcount += 1

    # Send file from filesystem to client
    def put_http_file(self, fname, content="text/html; charset=utf-8", hdr=""):
        try:
            f = open(fname)
        except:
            f = None
        if not f:
            self.put_http_404()
        else:
            flen = os.stat(fname)[6]
            resp = HTTP_OK + CONTENT_LEN%flen + CONTENT_TYPE%content + hdr + HEAD_END
            self.send_data(self.client_sock, resp)
            n = 0
            while n < flen:
                data = f.read(MAX_SPI_DLEN)
                self.send_data(self.client_sock, data)
                n += len(data)
            self.send_end(self.client_sock)

# Initialise TCP server, return class instance
def server_init():
    print("Connecting to %s..." % WIFI_SSID)
    e = ESP32()
    status = 0
    while status != STATUS_OK:
        if status==0 or status==STATUS_FAIL:
            e.connect(WIFI_SSID, WIFI_PASS)
            utime.sleep_ms(2000)
        status = e.check_wifi_status()
    e.start_server(HTTP_PORT)
    while not e.get_server_status():
        pass
    ip_addr = e.get_ip_address()
    print("Server socket {0}, {2}.{3}.{4}.{5}:{1}".format(e.server_sock, HTTP_PORT, *ip_addr))
    return e

if __name__ == "__main__":
    esp = server_init()
    adcs = [machine.ADC(pin) for pin in ADC_PINS]
    while True:
        req = esp.get_http_request()
        if req:
            r = req.split("\r")[0]
            print(r, end="")
            if ICON_FNAME in r:
                print(": not found")
                esp.put_http_404()
            elif TEST_FNAME in r:
                print(": test page")
                heads = ["GP%u" % pin for pin in ADC_PINS]
                vals = [("%1.3f" % (adc.read_u16() * ADC_SCALE)) for adc in adcs]
                th = "<tr><th>" + "</th><th>".join(heads) + "</th></tr>"
                tr = "<tr><td>" + "</td><td>".join(vals) + "</td></tr>"
                table = "<table><caption>ADC voltages</caption>%s</table>" % (th+tr)
                esp.put_http_text(TEST_PAGE % table)
            elif DATA_FNAME in r:
                print(": data file")
                esp.put_http_file(DIRECTORY+DATA_FNAME, "text/csv", DISABLE_CACHE)
            else:
                print(": index file")
                esp.put_http_file(DIRECTORY+INDEX_FNAME)
        utime.sleep_ms(10)

#EOF



