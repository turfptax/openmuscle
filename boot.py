# Test boot for masic functions for esp32-s2-mini
import omwap
import time
import machine
from machine import Pin, ADC
import socket

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
hall = [machine.ADC(Pin(3)),machine.ADC(Pin(5)),machine.ADC(Pin(7)),machine.ADC(Pin(9))]
oo = 0

for i in hall:
  print('hall[' + str(oo) + ']:',i.read())
  oo += 1

#I2C pin allocation test
#print('i2c test pins')
#i2c = machine.I2C(scl=machine.Pin(33), sda=machine.Pin(35))
#https://www.dfrobot.com/blog-608.html


throw(5)







