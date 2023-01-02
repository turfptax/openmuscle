#OpenMuscle - OpenHand V1.0.0
# 4 Finger Target Value Acquirer

import machine
import time
import network
import socket


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
zero = [0,0,0,0]
max = [0,0,0,0]
hall = []

# Pin 2 shorted so moved to 0 skip 1 & 2
for i in range(0,6):
  if i != 1 and i != 2:
    temp = machine.ADC(machine.Pin(i))
    #important to read the value properly
    temp.atten(machine.ADC.ATTN_11DB)
    hall.append(temp)
    print(i,temp.read())
    
def callibrate(vals,hall=hall):
  for i,x in enumerate(hall):
    vals[i] = x.read()
    print(i,x,vals[i])
  return(vals)

def read_all(hall=hall):
  for i,x in enumerate(hall):
    print(i,x,x.read())

  
zero = callibrate(zero)
print(zero)

print('Running loop')
for i in range(3):
  print('-------')
  read_all()
  time.sleep(1)
 

################
def initNETWORK():
  #need optional backup UDP repl if can't connect
  #primary and secondary networks
  #if primary then try secondary dev wifi access point
  wlan = network.WLAN(network.STA_IF) 
  wlan.active(False)
  wlan.active(True)
  wlan.config(txpower=8.5)
  time.sleep(2)
  print('connecting to wifi now')
  wlan.connect('OpenMuscle','3141592653')
  while not wlan.isconnected():
    pass
  print('assinging port and bind')
  port = 3145
  print('network config: ',wlan.ifconfig())
  print('network connected[Y]')
  s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  return(s,wlan)
#s.bind(('192.168.103.203',port))

s,wlan = initNETWORK()

#Version 5.3.0 miswired second two elements on hardware 0-11
# 0-5 top circular band on hexigon 1 per cell
# 6-11 bottom circular band on hexigon 1 per cell
cells = [hall[3],hall[2],hall[1],hall[0]]

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
  print('NTP Time [f]')
  print('failed to set NTP time')

#Gather send

#Declare temp var to write to text file

#packet length
plen = 10
#packet iterator
pi = 0
calib = [0,0,0,0]

#stop white loop for 10
time.sleep(10)


def mainloup(calib=calib,pi=pi,plen=plen,led=led,cells=cells,a=b):
  count = 0
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
    packet['id'] = '4-soma'
    packet['ticks'] = time.ticks_ms()
    packet['time'] = time.localtime()
    
    if pi == 0:
      print("No calibration just raw data")
      calib = calibrate(data)
      #print(calib)
    if pi >= 10:
      print(count,status)
      count += 1
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
      status = str(packet)
    except:
      status = 'failed'

mainloup()
print('this is after mainloup()')




