import socket
import time

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    return s.getsockname()[0]

# Could have used local host
ip_address = get_ip_address()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#packet["id"] = "OM-Band12"
#packet["ticks"] = time.ticks_ms()
#packet["time"] = time.localtime()
#packet['data'] = data

text_file = open('Data-Captures/capture_12.txt','r')

for i in text_file.read().split('\n'):
    time.sleep(.009)
    raw_data = i.encode('utf-8')
    s.sendto(raw_data,(ip_address,3145))
    




