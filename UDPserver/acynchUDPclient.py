#!python3
#Asycnch UDP REPL Client
#11-22-2022
#TURFPTAx

import socket
import os, sys
import time

#default communication port
#Needs to be changed on both client and server if modified
PORT = 3145

if len(sys.argv) == 3:
    server_ip_address = sys.argv[1]
    server_port = sys.argv[2]
else:
    print('Run like: acynchUDPserver.py <arg1: server ip> <arg2: UDP port>')
    server_ip_address = '192.168.89.120'
    server_port = 3145
    print(f'using default server ip: {server_ip_address}')
    print(f'using defaul port: {server_port}')

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    return s.getsockname()[0]
    

client_ip = get_ip_address()
print(f'client ip address: {client_ip}')

# setup sending socket object: s
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


# setup receiving socket binded object r
r = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
r.bind((client_ip,PORT))

while True:
    #data = input(f'UDP Command {server_ip_address}:{server_port} ')
    s.sendto(bytes('hi0',"utf-8"),(server_ip_address,server_port))
    print(f'sent hi0 to {server_ip_address}:{server_port}')
    #waits for a reply
    r.settimeout(2)
    try:
        reply,addr = r.recvfrom(1024)
        print(reply.decode('utf-8'))
    except:
        print('timed out')
    
    

         
