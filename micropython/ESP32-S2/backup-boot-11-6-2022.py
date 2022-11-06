# MARK2 5.3.2 second one made -11-4-2022
# OpenMuscle Sensor Band 5.3.0
# UDP send 
# super rough working code not pythonic
# Test boot for masic functions for esp32-s2-mini
# need to have omwap file on ESP32-S2
# omwap Open Muscle Wireless Access Point - throughput not good enough for UDP packets on ESP32-C3 without more testing
#import omwap

# Simplify machine and from machine reduntant
import time
import machine
from machine import Pin, ADC, I2C
import socket
import network
import ssd1306

ledPIN = 15
sclPIN = 33
sdaPIN = 34
oledWIDTH = 128
oledHEIGHT =  32
led = False


# Code feedback through onboard LED GPIO 15 or ledPIN

def initLED(ledPIN):
  try:
    led = Pin(ledPIN,Pin.OUT)
    print('led initialized!')
    print('led =',led)
    try:
      throw(1)
    except:
      print('couldnt use throw(1)')
  except:
    print('led did not work :(')
    led = False
  return(led)

led = initLED(ledPIN)

def throw(amt, led=led):
  if led:
    for i in range(amt):
      led.value(1)
      time.sleep(.66)
      led.value(0)
      time.sleep(.33)
  else:
    print('throw(n) n=',amt)

ram = []

print('trying to init oled')
def initOLED(scl=Pin(sclPIN),sda=Pin(sdaPIN),led=led,w=oledWIDTH,h=oledHEIGHT):
  print('scl = ',scl)
  print('sda = ',sda)
  oled = False
  i2c = False
  try:
    i2c = machine.I2C(scl=scl,sda=sda)
  except:
    print('i2c failed check pins scl sda')
    try:
      print('i2c.scan() = ',i2c.scan())
    except:
      print('i2c.scan() failed')
  if i2c:
    try:
      oled = ssd1306.SSD1306_I2C(w,h,i2c)
      print("SSD1306 initialized[Y]")  
      print('oled = ',oled)
    except:
      print("failed to initialize onboard SSD1306")
  return oled

oled = initOLED()

def frint(text,oled=oled,ram=ram):
  if oled:
    if text:
      text = str(text)
      if len(text) <= 16:
        ram.append(text)
      else:
        ram.append(text[0:5]+'..'+text[len(text)-9:])
    oled.fill(0)
    n = 0
    for i in ram[-4:]:
      oled.text(i,0,n*8)
      n+=1
    if len(ram) > 9:
      ram = ram[-9:0]
    oled.show()
  else:
    print('frint(t) t=',text)

# Start using frint to log and print backs up if frint doesnt work
if oled:
  frint('SSD1306 initialized[Y]')
else:
  print('oledINIT failed')

#Setup basic ADC pin read array test
print('setting up 4 hall array: hall[0-18]')
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

frint('hall array setup[Y]')
throw(5)

#need encrypted method of store/retrieve
#current wifi connection because of ease of use
sta_if = network.WLAN(network.STA_IF) 
sta_if.active(False)

if not sta_if.isconnected():
  print('connecting to network...')
  if sta_if.isconnected() == False:
    sta_if.active(True)
  sta_if.connect('OpenMuscle','3141592653')
  while not sta_if.isconnected():
    pass

print('assing port and bind')
port = 5005
print('network config: ',sta_if.ifconfig())
frint('network connected[Y]')
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.bind(('192.168.103.203',port))

# Cell organization
# old mehtod of storing adc objects
#cell0 = [hall[5],hall[2]]
#cell1 = [hall[4],hall[1]]
#cell2 = [hall[3],hall[0]]
#cell3 = [hall[16],hall[17]]
#cell4 = [hall[11],hall[8]]
#cell5 = [hall[12],hall[9]]

#Version 5.3.0 miswired second two elements on hardware 0-11
# 0-5 top circular band on hexigon 1 per cell
# 6-11 bottom circular band on hexigon 1 per cell
cells = [hall[5],hall[4],hall[3],hall[16],hall[11],hall[12],hall[1],hall[2],hall[0],hall[17],hall[8],hall[9]]

#inital hall sensor ADC calibration
# grabs first few inputs and reduces the value 
def calibrate(data):
  calib = []
  better = data.split(',')
  for x in better:
    if x:
        calib.append(int(x))
  return calib

try:
  import ntptime
  ntptime.settime()
  time.localtime()
  print(time.localtime())
except:
  frint('NTP Time [f]')
  print('failed to set NTP time')

#Gather send
#Declare temp var to write to text file

#packet length
plen = 10
#packet iterator
pi = 0
calib = [0,0,0,0,0,0,0,0,0,0,0,0]

#stop white loop for 10
time.sleep(10)


frint('key input needed')
input()

while True:
  data = ''
  for i in range(len(cells)):
    data += str(cells[i].read()-calib[i]) + ','
  if pi == 0:
    calib = calibrate(data)
    print(calib)
  if pi >= 10:
    pi = 1
  else:
    pi += 1
  #Append the cycle with : deliminer delimeter
  try:
    #UDP recepient address
    #Work on dynamic setup protocol
    s.sendto(data.encode('utf-8'),('192.168.1.32',3145))
    time.sleep(.2)
  except:
    print('failed')

