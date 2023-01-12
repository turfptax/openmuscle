


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
try:
  import ssd1306
except:
  print("failed to import ssd1306")

ledPIN = 15
sclPIN = 33
sdaPIN = 34
oledWIDTH = 128
oledHEIGHT =  32
button_leftPIN = 36
button_rightPIN = 35
led = False
b_left = machine.Pin(button_leftPIN,machine.Pin.IN,machine.Pin.PULL_UP)
b_right = machine.Pin(button_rightPIN,machine.Pin.IN,machine.Pin.PULL_UP)


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
    print('f:> ',ram[-1])
  else:
    print('f:< ',text)

# Start using frint to log and print backs up if frint doesnt work
if oled:
  frint('SSD1306 initialized[Y]')
else:
  print('oledINIT failed')

#Setup basic ADC pin read array test
print('hall array: hall[0-18] hall[0] is None so pins match')
hall = [None]
for i in range(1,19):
  temp = machine.ADC(Pin(i))
  #important to read the value properly
  temp.atten(ADC.ATTN_11DB)
  hall.append(temp)


for i,x in enumerate(hall):
  print(i,x)

frint('hall array setup[Y]')
throw(5)

#need encrypted method of store/retrieve
#current wifi connection because of ease of use
def initNETWORK(a=b_left,b=b_right):
  #need optional backup UDP repl if can't connect
  #primary and secondary networks
  #if primary then try secondary dev wifi access point
  wlan = network.WLAN(network.STA_IF) 
  wlan.active(False)
  if not wlan.isconnected():
    frint('connecting to network...')
    if wlan.isconnected() == False:
      wlan.active(True)
    wlan.connect('OpenMuscle','3141592653')
    while not wlan.isconnected():
      pass

  print('assing port and bind')
  port = 3145
  print('network config: ',wlan.ifconfig())
  frint('network connected[Y]')
  s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  return(s,wlan)
#s.bind(('192.168.103.203',port))

s,wlan = initNETWORK()

#Version 5.3.0 miswired second two elements on hardware 0-11
# 0-5 top circular band on hexigon 1 per cell
# 6-11 bottom circular band on hexigon 1 per cell
# 5.4.2 6x2 left to right also works for 12x1 left to right
cells = [hall[6],hall[2],hall[5],hall[3],hall[4],hall[1],hall[16],hall[17],hall[12],hall[9],hall[13],hall[10]]

#inital hall sensor ADC calibration
# grabs first few inputs and reduces the value 

def calibrate(data):
  calib = []
  for x in data:
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


def mainloup(calib=calib,pi=pi,plen=plen,oled=oled,ram=ram,led=led,cells=cells,a=b_left,b=b_right):
  exit_bool = False
  button_thresh = 0
  while not exit_bool:
    if a.value() == 0:
      button_thresh += 1
    else:
      button_thresh += -1
    if button_thresh > 20:
      exit_bool = True
    elif button_thresh < 0:
      button_thresh = 0
    packet = {}
    data = []
    for i in range(len(cells)):
      data.append(cells[i].read()-calib[i])
    packet["id"] = "OM-Band12"
    packet["ticks"] = time.ticks_ms()
    packet["time"] = time.localtime()
    if pi == 0:
      print("No calibration just raw data")
      #calib = calibrate(data)
      #print(calib)
    if pi >= 10:
      pi = 1
    else:
      pi += 1
    #Append the cycle with : deliminer delimeter
    packet['data'] = data
    raw_data = str(packet).encode('utf-8')
    try:
      #UDP recepient address
      #Work on dynamic setup protocol
      s.sendto(raw_data,('192.168.1.32',3145))
    except:
      print('failed')

mainloup()
frint('this is after mainloup()')











