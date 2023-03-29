import socket
import time

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    return s.getsockname()[0]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#packet["id"] = "OM-Band12"
#packet["ticks"] = time.ticks_ms()
#packet["time"] = time.localtime()
#packet['data'] = data

text_file = open('datasetONE-END.txt','r')

for i in text_file.read().split('\n'):
    time.sleep(.009)
    raw_data = i.encode('utf-8')
    s.sendto(raw_data,('192.168.1.32',3145))
    




