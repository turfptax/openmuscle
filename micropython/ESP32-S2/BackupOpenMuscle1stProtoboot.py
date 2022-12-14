



# Test boot for masic functions for esp32-s2-mini
# need to have omwap file on ESP32-S2
#import omwap
import time
import machine
from machine import Pin, ADC
import socket
import network


#Flash led on pin 15 10 times
#Bootup time grace period to flash ESP32
led = Pin(15,Pin.OUT)
for i in range(10):
  led.value(1)
  time.sleep(.2)
  led.value(0)
  time.sleep(.1)

# Code feedback through onboard LED GPIO 15
def throw(amt, led=led):
  for i in range(amt):
    led.value(1)
    time.sleep(.33)
    led.value(0)
    time.sleep(.33)

#Run Wireless Access Point for Test Server
#print('opening Open Muscle Wifi Access Point lib: omwap.py')
#omwap

#Setup basic ADC pin read array test
print('setting up 4 hall array: hall[0-3]')
hall = []
for i in range(1,19):
  temp = machine.ADC(Pin(i))
  #important to read the value properly
  temp.atten(ADC.ATTN_11DB)
  hall.append(temp)


oo = 0
for i in hall:
  print('hall[' + str(oo+1) + ']:',i.read())
  oo += 1

#I2C pin allocation test
#print('i2c test pins')
#i2c = machine.I2C(scl=machine.Pin(33), sda=machine.Pin(35))
#https://www.dfrobot.com/blog-608.html


throw(5)



sta_if = network.WLAN(network.STA_IF) 
sta_if.active(False)

if not sta_if.isconnected():
  print('connecting to network...')
  sta_if.active(True)
  sta_if.connect('OpenMuscle','3141592653')
  while not sta_if.isconnected():
    pass

print('assing port and bind')
port = 3149
print('192.168')
print('network config: ',sta_if.ifconfig())
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.bind(('192.168.103.203',port))

cell0 = [hall[5],hall[2]]
cell1 = [hall[4],hall[1]]
cell2 = [hall[3],hall[0]]
cell3 = [hall[16],hall[17]]
cell4 = [hall[11],hall[8]]
cell5 = [hall[12],hall[9]]

while True:
  data = ''
  for i in range(2):
    data += str(cell0[i].read()) + ','
    data += str(cell1[i].read()) + ','
    data += str(cell2[i].read()) + ','
    data += str(cell3[i].read()) + ','
    data += str(cell4[i].read()) + ','
    data += str(cell5[i].read()) + ','
  #print('data')
  try:
    s.sendto(data.encode('utf-8'),('192.168.1.32',3145))
  except:
    print('failed')









