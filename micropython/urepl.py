# Simple urepl like module
# takes care of connecting to wifi or creating your own
# written for the Rapsberry Pi Pico W
# requires the frint dependancy to allow for print over udp

import gc
import socket
import network
import time

# Network Setup
global connection_type
global ssid
global password

# Server Client Setup
global server_ip
global client_ip
global port
global timeout

# Frint Setup
global ram
global cur
global buff


# Frint Arrays/variables No need to change
ram = []
cur = 0
buff = ['blank']
# Default Network to connect using wificonnect()
# Change these settings or use the built in functions
connection_type = 'Not Connected'
ssid = 'OpenMuscle'
password = '3141592653'
port = 3145
server_ip = '0.0.0.0'
client_ip = '192.168.1.32'
timeout = 15


def wificonnect(ssid=ssid,password=password):
    print('Use: like urepl.wificonnect(SSID,Password)')
    print('otherwise uses default global ssid,password')
    print('returns wlan object from network')
    global server_ip
    global connection_type
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    wlan.connect(ssid,password)
    while not wlan.isconnected():
        pass
    server_ip = wlan.ifconfig()[0]
    print('Wifi Connected!!')
    print(f'SSID: {ssid}')
    print('Local Ip Address, Subnet Mask, Default Gateway, Listening on...')
    print(wlan.ifconfig())
    connection_type = 'Wireless Client'
    return wlan

def wap(pico_ssid = "PicoW",pico_pass = "picopico"):
    global server_ip
    global connection_type
    print('Use: like urepl.wap(SSID,Password)')
    print('otherwise uses default Picow,picopico')
    print('returns network wap object')
    #Create a network and WAP Wireless Access Point
    wap = network.WLAN(network.AP_IF)
    wap.config(essid=pico_ssid,password=pico_pass)
    wap.active(False) #rare instances keep this on
    wap.active(True)
    while wap.active == False:
        pass
    print('Wireless Access Point (WAP) Created!!')
    print(f'SSID: {pico_ssid}')
    print(f'PASSWORD: {pico_pass}')
    print('Local Ip Address, Subnet Mask, Default Gateway, Listening on...')
    server_ip = wap.ifconfig()[0]
    print(wap.ifconfig())
    connection_type = "Wireless Access Point"
    return wap

def send(data):
    global client_ip
    global port
    d = b''
    d += data
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    destination = (client_ip,port)
    print(s)
    s.sendto(d,destination)
    s.close
    gc.collect()

# Akin to input() on normal python
# Will open a UDP socket and wait for a packet
# Will keep code from running 
def receive():
    data = 'print("oopsydaisy")'
    global client_ip
    global port
    global server_ip
    global timeout
    print('Use like urepl.receive(server_ip,port)')
    r = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    r.bind((server_ip,port))
    r.settimeout(15)
    print(f'waiting to receive on {server_ip}:{port}')
    try:
        data,addr = r.recvfrom(1024)
        client_ip = addr[0]
    except:
        print('timeout exceeded or recvfrom err')
        r.close()
    r.close()
    gc.collect()
    return data

def printdetails():
    global ssid
    global server_ip
    global password
    global client_ip
    global port
    global timeout
    global connection_type
    print(f'connection_type: {connection_type}')
    print(f'ssid: {ssid}')
    print(f'server_ip: {server_ip}')
    print(f'client_ip: {client_ip}')
    print(f'port: {port}')
    print(f'timeout: {timeout}')
    
def set_client_ip(client):
    global client_ip
    client_ip = client
    print(f'You set the client_ip to: {client_ip}')
    printdetails()

def set_port(p):
    global port
    port = p
    print(f'You set the port to: {port}')
    printdetails()

def set_timeout(t):
    global timeout
    timeout = t
    print(f'You set the timeout to: {timeout}')
    printdetails()

def start():
    gc.collect()
    end_session = False
    while not end_session:
        reply = receive()
        try:
            frint(exec(reply))
        except:
            frint(str(reply))
        send(bytes(str(frint.getbuff()),'utf-8'))
        if reply == b'stop':
            end_session = True
            
def frint(data):
    global ram
    global cur
    if type(data) is type(None):
        if cur != 0:
            return printram(0-cur)
    elif type(data) == str:
        ram.append(data)
        cur += 1
        return ram[-1]
    elif type(data) == list:
        for i in data:
            frint(i)
        return printram(0-cur)
    elif type(data) == int or type(data) == bool or type(data) == float:
        ram.append(str(data))
        cur += 1
        return ram[-1]

#runs everytime then end of a list or command happens
def printram(ammount):
    global ram
    global buff
    buff.append(ram)
    return(buff[-1])

# Only runs by outside call
def getram():
    global ram
    return(ram[-1])

def getbuff():
    global buff
    return(buff[-1])
    
    

print('--urepl--')