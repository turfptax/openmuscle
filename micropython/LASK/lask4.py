
#OpenMuscle - OpenHand V1.0.0
# 4 Finger Target Value Acquirer

import machine
import time
import network
import socket
import ssd1306
import gc

# Globals
# defin ADCs and make loud
zero = [0,0,0,0]
hall = []
mins = [4156, 3961, 3617, 4157]

maxes = [5064, 5241, 5077, 5233]
ram = []
led = False
ledPIN = 15
sclPIN = 33
sdaPIN = 34
oledWIDTH = 128
oledHEIGHT =  32
startPIN = 7
selectPIN = 8
upPIN = 9
downPIN = 10
s,wlan = False,False

#Button variables
start = machine.Pin(startPIN,machine.Pin.IN,machine.Pin.PULL_UP)
select = machine.Pin(selectPIN,machine.Pin.IN,machine.Pin.PULL_UP)
up = machine.Pin(upPIN,machine.Pin.IN,machine.Pin.PULL_UP)
down = machine.Pin(downPIN,machine.Pin.IN,machine.Pin.PULL_UP)

#Startup Sequence
led = machine.Pin(15,machine.Pin.OUT)



def blink(x):
  for _ in range(x):
    led.value(1)
    time.sleep(.3)
    led.value(0)
    time.sleep(.2)

blink(7)

def initOLED(scl=machine.Pin(sclPIN),sda=machine.Pin(sdaPIN),led=led,w=oledWIDTH,h=oledHEIGHT):
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
      ram = ram[-9:]
    gc.collect()
    oled.show()
    print('f:> ',ram[-1])
  else:
    print('f:< ',text)


def initNETWORK():
  #need optional backup UDP repl if can't connect
  #primary and secondary networks
  #if primary then try secondary dev wifi access point
  wlan = network.WLAN(network.STA_IF) 
  wlan.active(False)
  wlan.active(True)
  time.sleep(1)
  frint('connecting to wifi now')
  wlan.connect('OpenMuscle','3141592653')
  while not wlan.isconnected():
    pass
  print('assinging port and bind')
  port = 3145
  frint(f'network config:{wlan.ifconfig()}')
  frint('network connected[Y]')
  s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  return(s,wlan)
  
def read_all(hall=hall):
  reads = []
  for i,x in enumerate(hall):
    reads.append(x.read())
    print(i,x,reads[-1])
  return(reads)
    
    

def callibrate(hall=hall,start=start):
  global mins
  global maxes
  frint('plese RELEASE')
  frint('all depressors')
  time.sleep(2)
  mins = []
  maxes = []
  for i,x in enumerate(hall):
    maxes.append(x.read())
    print(i,x)
  frint('please PRESS')
  frint('all dep & strt')
  end = False
  while not end: 
    if start.value() == 0:
      end = True
      for i,x in enumerate(hall):
        mins.append(x.read())
        print(i,x)



def taskbar(hall=hall,oled=oled):
  oled.fill(0)
  oled.text('OM-LASK4 V1',0,0,1)
  x = 87
  y = 17
  global mins
  global maxes
  ammount = 5
  oled.fill_rect(0+x,0+y,40,14,1)
  oled.fill_rect(1+x,1+y,38,12,0)
  for i,z in enumerate(hall):
    div_top = (z.read()-mins[i])
    div_bottom = (maxes[i]-mins[i])
    if div_bottom == 0:
      div_bottom = 1
    ch = int((div_top/div_bottom)*12)
    r_x = ((i+1)*7)+x
    r_y = 13-(ch)+y
    oled.fill_rect(r_x,r_y,5,ch,1)
    oled.text(str(i+1),i*20,16,1)
    oled.text(str(ch*8),i*20,24,1)
  oled.show()
  
  

frint('OM-LASK4 Boot')




for i in range(2,6):
  temp = machine.ADC(machine.Pin(i))
  temp.atten(machine.ADC.ATTN_11DB)
  hall.append(temp)

cells = [hall[0],hall[1],hall[2],hall[3]]
read_all()

plen = 10
pi = 0
calib = [0,0,0,0]
blink(2)

def drawMenu():
  frint('OM-LASK4 Menu')


def fastRead(s=s):
  packet = {}
  data = []
  for i in range(len(cells)):
      data.append(cells[i].read()-calib[i])
  packet['id'] = '4-soma'
  packet['ticks'] = time.ticks_ms()
  packet['time'] = time.localtime()
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


def mainMenu():
  global start
  global select
  global up
  global down
  global oled
  menu = [['[0] Wifi Connect',0,0],['[1] Callibrate',1,1],['[2] UDP Send',2,1],['[3] Exit',3,1]]
  end = False
  while not end:
    oled.fill(0)
    for i,x in enumerate(menu):
      oled.fill_rect(0,i*8,128,8,abs(x[2]-1))
      oled.text(x[0],0,i*8,x[2])
    oled.show()
    if start.value() == 0 and menu[0][2] == 0:
      global s
      global wlan
      frint('init network')
      s,wlan = initNETWORK()
      cells = [hall[3],hall[2],hall[1],hall[0]]
      try:
        import ntptime
        ntptime.settime()
        time.localtime()
        print(time.localtime())
      except:
        frint('NTP Time [f]')
        frint('failed to set NTP time')
      return
    if start.value() == 0 and menu[3][2] == 0:
      return
    if start.value() == 0 and menu[1][2] == 0:
        callibrate()
        return
    if up.value() == 0 or down.value() == 0:
      for i,x in enumerate(menu):
        if x[2] == 0:
          if up.value() == 0:
            menu[i][2] = 1
            menu[i-len(menu)+1][2] = 0
            time.sleep(.3)
          if down.value() == 0:
            menu[i][2] = 1
            menu[i-1][2] = 0
            time.sleep(.3)
            
    




def mainloup(pi=pi,plen=plen,led=led,cells=cells,start=start,select=select,up=up,down=down):
  count = 0
  exit_bool = False
  button_thresh = 0
  while not exit_bool:
    if up.value() == 0 or down.value() == 0:
      mainMenu()
    if select.value() == 0:
      button_thresh += 1
    else:
      button_thresh += -1
    if button_thresh > 20:
      exit_bool = True
    elif button_thresh < 0:
      button_thresh = 0
    if pi == 0:
      frint('first run')
      #callibrate()
    if pi >= 10:
      taskbar()
      count += 1
      pi = 1
    else:
      pi += 1
    

mainloup()
print('this is after mainloup()')



