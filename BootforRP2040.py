

#-- Main program
import machine, ssd1306, os

import network
import time
global ram
global cur
# MQTT requirements:
import ubinascii
import micropython
import esp
from umqtt.simple import MQTTClient
from machine import I2C, Pin



esp.osdebug(None)
import gc
gc.collect()
mqtt_server = '172.16.2.184'
client_id  = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_sub = b'hello'
last_message = 0
message_interval = 5
counter = 0

ram = ['1','2','3','4','5','6','7','8','9','0']
cnt = 0

print('*****************************************************')
print('                init display                         ')
#Initialize the 128*64 SSD1306 screen pins are 15 & 4 onb
print('setting up pins 15 and 4 and trying to reset 16')
scl = machine.Pin(15,mode=machine.Pin.OUT,pull=machine.Pin.PULL_UP)
sda = machine.Pin(4,mode=machine.Pin.OUT,pull=machine.Pin.PULL_UP)
pin = machine.Pin(16,mode=machine.Pin.OUT,pull=machine.Pin.PULL_UP)
pin.value(0)
#pin.value(1)

i2c = machine.I2C(scl=scl, sda=sda)
print('i2c.scan() output: ', i2c.scan())
#i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))

# Tip to get the oled=ssd1306 to work on ESP32

scl.value(0)
sda.value(0)
scl.value(1)
sda.value(1)
print('i2c.scan() after 16 rst: ', i2c.scan())


#initiate the display 128 x 64 HITEK ....SSD1206
try:
  oled = ssd1306.SSD1306_I2C(128,64,i2c)
  frint("SSD1306-Good [1]")
  print("ssid1306 - success")
except:
  print("failed to initialize onboard SSD1306")


#Functions

def makeshift(ms):
  for i in ms:
    frint(i)

def joinNetwork():
  sta_if = network.WLAN(network.STA_IF)
  frint('StartNetwork [*]')
  sta_if.active(True)
  time.sleep(3)
  sta_if.connect(ssid,pow)
  print('IP address:',sta_if.ifconfig()[0])
  if sta_if.ifconfig()[0]=="0.0.0.0":
    frint('NetFail retry[0]')
    joinNetwork()
  return(sta_if.ifconfig()[0])
  

def bottomBar():
  global ram
  # get rid of glitches from screen refreshes
  # mostly to try to rid memory allocation
  # not sure how upython handles memory
  # ----Thus why i learned python ----
  if len(ram) > 255:
    ram = ram[128:255]
  print('Heads Up Display')
  for x in range(0,len(ram)-1):
    oled.pixel(x,64,1)
    oled.pixel(int(x/2),63,1)
    oled.pixel(int(x/4),62,1)
    oled.pixel(int(x/8),61,1)
  print('bottomBar************************************')
  oled.show()
    
def frint(text):
  global ram
  global cur
 
  lent = 0
  # converting no
  if type(text) != str:
    text = str(text)
  
  oled.fill(0)
  l = len(text)
  c = 0
  x = 0

  buff = ''
  outp = []
  if l > 16:
    for i in text:
      if c < 15:
        buff += i
        c += 1
      else:
        outp.append(buff+i)
        buff = ''
        c = 0
        x += 1
    if buff != '':
      outp.append(buff)
      

  else:
    outp.append(text)
  lent = len(outp)
  
  #print('outp')
  #print(outp)
  
  #cur += 1

  for z in range(len(outp)):
    ram.append(outp[z])
    #oled.text(outp[z],0,z*10
  for z in range(0,6):
    ll = len(ram)-(6-z)
    #print("ll",ll,"ramll",ram[ll])
    oled.text(ram[ll],0,z*10)
  
  bottomBar()
  #oled.show()
  return outp,'Return of frints buff'
  # Print the Bottom Bar UI 
  
  



frint('wait for net [0]')
time.sleep(3)

iffyIP = joinNetwork()
frint(iffyIP)
frint('Net Success! [1]')

button = machine.Pin(21,machine.Pin.IN, machine.Pin.PULL_UP)
print('button mapped')



#import sendmail
frint('Start MQTT   [*]')
# Modify below section as required
CONFIG = {
     # Configuration details of the MQTT broker
     "MQTT_BROKER": "172.16.2.184",
     "USER": "qutte",
     "PASSWORD": "rhdchc302",
     "PORT": 1883,
     "TOPIC": b"doorstat",
     # unique identifier of the chip
     "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}
 
# Method to act based on message received   
def onMessage(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))
    if msg == b"on":
        print('LED: ON')
    elif msg == b"off":
        print('LED: OFF')
    
      
def listen():
    global interruptCounter
    #Create an instance of MQTTClient 
    client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
    # Attach call back handler to be called on receiving messages
    client.set_callback(onMessage)
    client.connect()
    client.publish(CONFIG['TOPIC'], "ESP32 is Connected")
    client.publish(CONFIG['TOPIC'], "off")
    client.subscribe(CONFIG['TOPIC'])
    print("ESP32 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG['TOPIC']))
    frint("MQTTConnected[1]")
    # Button
    button = machine.Pin(21,machine.Pin.IN, machine.Pin.PULL_UP)
    print('button mapped')
    presses = 0
    frint('Start Main   [*]')
    old3 = [1,1,1]
    r = 0
    v = 1
    try:
        while True:
            #msg = client.wait_msg()
            msg = (client.check_msg())

            if button.value() == 0 and 0 not in old3:
              v = 0
              print("Button pressed")
              frint("button pressed")
              client.publish(CONFIG['TOPIC'], b"on")
              import doorbellemail
            elif 0 in old3 and 1 in old3:
              v = 1
              client.publish(CONFIG['TOPIC'], b"off")
            old3[r] = v
            r += 1

            if r == 3:
              r = 0
            time.sleep_ms(500)
    finally:
        client.disconnect()  

listen()        














