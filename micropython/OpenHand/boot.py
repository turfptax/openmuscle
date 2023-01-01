#OpenMuscle - OpenHand V1.0.0
# 4 Finger Target Value Acquirer

import machine
import time

led = machine.Pin(7,machine.Pin.OUT)

# DON"T ASSIGN PIN 7 TO BUTTON!!! see line above
b = machine.Pin(8,machine.Pin.IN,machine.Pin.PULL_UP)

def blink(x):
  for _ in range(x):
    led.value(1)
    time.sleep(.3)
    led.value(0)
    time.sleep(.2)

blink(7)

# defin ADCs and make loud
zero = []
max = []
hall = []
for i in range(2,6):
  temp = machine.ADC(machine.Pin(i))
  #important to read the value properly
  temp.atten(machine.ADC.ATTN_11DB)
  hall.append(temp)
  zero.append(temp.read())
  print(i,temp.read())
  
def callibrate(hall=hall):
  for i,x in enumerate(hall):
    zero[i] = x.read()
    print(i,x,zero[i])
    
    
    
callibrate()
print(zero)
  
  
 




