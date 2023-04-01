#!python3

# Mimics just a blank Lask packet for demo
# Model is trained with matchning algorithm
# This sends packet values over UDP
# Change them to be whatever you wish



import socket
import time


packet = {'id': 'OM-LASK4',
          'time': (2023, 3, 28, 22, 44, 34, 1, 87),
          'data': [5555, 5555, 5555, 5555],
          'ticks': 231140,
          'rec_time': 0.0141592653589}

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    return s.getsockname()[0]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#packet["id"] = "OM-Band12"
#packet["ticks"] = time.ticks_ms()
#packet["time"] = time.localtime()
#packet['data'] = data

text_file = open('training_file10.txt','r')

for i in range(1000):
    time.sleep(.009)
    packet["time"] = time.localtime()
    raw_data = packet.encode('utf-8')
    s.sendto(raw_data,('192.168.1.32',3145))
    




