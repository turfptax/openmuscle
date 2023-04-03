import socket
import numpy as np
import pygame as pg
import csv
import sys
import os
import time
import ast
import math

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Load the saved model from the file
with open('live_capture.pkl', 'rb') as f:
    loaded_model = pickle.load(f)




# Data Processing variables and Functions ---
found_count = 0
found = []
lask = []
band = []
last_pair = None

def send_chunk(data):
    global lask
    global band
    temp = []
    # array structure [signal_int * count,received time float]
    #print('data:',data)
    if 'OM-LASK' in data['id']:
        for i in data['data']:
            temp.append(i)
        temp.append(data['rec_time'])
        lask.append(temp)
    elif 'OM-Band' in data['id']:
        for i in data['data']:
            temp.append(i)
        temp.append(data['rec_time'])
        band.append(temp)

def check_chunk():
    global lask
    global band
    global last_pair
    global found
    global found_count
    dindexL =[]
    dindexB =[]
    if len(band) > 10:
        for i,x in enumerate(band):
            time = x[-1]
            for o,z in enumerate(lask):
                if abs(z[-1] - time) < .02:
                    found.append([x,z])
                    found_count += 1
                    last_pair = z[-1]
                    del lask[o]
    for i in dindexB:
        del band[i]
    if len(band) > 20:
        band = band[-10:]
    if len(lask) > 20:
        lask = lask[-10:]
    #if not len(found) % 1000:
        #print('found ammount: ',len(found))
# END Data Processing Variables and Functions ---


lpps = 0
bpps = 0

last_lask_packet = {'id': 'OM-LASK4', 'time': (2023, 1, 8, 22, 37, 28, 6, 8), 'data': [3, 1, 4, 5], 'ticks': 53249, 'rec_time': 0.0001}
last_band_packet = {'id': 'OM-Band12', 'time': (2023, 1, 8, 22, 37, 28, 6, 8), 'data': [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000], 'ticks': 2, 'rec_time': 0.0001}


max_samp = 6500
min_samp = 4000

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    return s.getsockname()[0]

#Get "IP address of Server" and also the "port number" from arg 1 and 2
if len(sys.argv) == 3:
    ip = sys.argv[1]
    port = int(sys.argv[2])
else:
    print('run like: python UDPserver.py <arg1: server ip> <arg2: UDPport>')
    local_ip = get_ip_address()
    port = 3145
    print('using {0} and 3145 '.format(local_ip))


### Create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (local_ip, port)
s.bind(server_address)
print(f'Server Address:{local_ip} Port:{port}')
print('Do Ctrl+c to exti the program !!')


### PYGAME SETUP
pg.font.init()
my_font = pg.font.SysFont('Courier New', 24)

#pygame width height etc
pg_width = 1200
pg_height = 800
screen_width = 640
screen_height = 480


#pygame init and screen declaration
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((pg_width,pg_height))

text_surface = my_font.render('OpenMuscle', False, (127,127,127))
screen.blit(text_surface, (200,200))
pg.display.update()

# Hari's Turf Hand
# Origin
x = int(pg_width/2) + 320
y = int(pg_height/2) + 240

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

finger_width = 51
finger_height = 120
finger_spacing = 10
palm_width = finger_spacing + 4*(finger_width+finger_spacing)
palm_height = 200
finger_length = [finger_height, int(finger_height*1.5), int(finger_height*1.8), int(finger_height*1.5)]
radius = 20
x_mod = 800
def yy(y):
    return screen_height-y

def drawLine(x1,y1, x2,y2, w, color):
    pg.draw.line(screen, color, (x1, yy(y1)), (x2, yy(y2) ), width=w, )
    #pg.display.update()

def drawDisc(x,y, dia, color):
    r = int(dia/2)
    pg.draw.ellipse(screen, color, (x-r, yy(y+r), dia,dia))
    #pg.display.update()

def drawRect(x,y,width,height, color):
    pg.draw.rect(screen, color, (x, yy(y)-height, width, height))
    #pg.display.update()

def drawRoundRect(x,y,width,height, r, color):
    pg.draw.rect(screen, color, (x+x_mod, yy(y)-height, width, height), border_radius=r)
    pg.display.update()

def drawPalm():    
    drawRoundRect(0,0, palm_width,palm_height, radius, WHITE)

def drawFinger(index, ratio):
    x = finger_spacing + finger_width/2 + index*(finger_width+finger_spacing)+x_mod
    y1 = palm_height-5
    y2 = palm_height + int(finger_length[index] * ratio)
    drawDisc(x,y2, finger_width, WHITE)
    drawLine(x,y1, x,y2, finger_width, WHITE)

def drawThumb():
    w2 = int(finger_width / math.sin(math.radians(45)))
    x1 = palm_width-int(w2/2)+x_mod
    y1 = int(palm_height/3)
    x2 = x1+finger_height-int(finger_width/2)
    y2 = y1+finger_height-int(finger_width/2)
    
    for i in range(-15,15):
        x3 = x2 + i
        y3 = y2 + i
        drawDisc(x3,y3, finger_width, WHITE)

    drawLine(x1,y1, x2,y2, w2, WHITE)

def drawHand(fingerRatios):
    #screen.fill(BLACK)
    r = pg.Rect(800,2,400,600)
    screen.fill((0,0,0), r)
    drawPalm()
    drawThumb()
    drawFinger(0, fingerRatios[0])
    drawFinger(1, fingerRatios[1])
    drawFinger(2, fingerRatios[2])
    drawFinger(3, fingerRatios[3])
    pg.display.update()
 
#----------------------------------








first_run = True
adc_dis = 65
pop = 4
buff = 25

def draw_signal(x0,y0,x,y,position,color,screen=screen):
    height = 40
    global max_samp
    global min_samp
    #if y0 < max_samp and y0 >= min_samp+150 and y0 < max_samp - 100:
    #    max_samp -= 100
    #elif y0 > max_samp:
    #    max_samp = y0
    #if y0 > min_samp and y0 <= max_samp+150 and y0 > min_samp +100:
    #    min_samp += 100
    # Row Multiply by position # * pixel height
    y0 = int(((y0-min_samp)/(max_samp-min_samp))*40)+(position*40)
    y = int(((y-min_samp)/(max_samp-min_samp))*40)+(position*40)
    # Left Padding
    x += 50
    x0 += 50
    pg.draw.line(screen,color,(x0,y0),(x,y),width=1)
    #if y < max_samp and y >= min_samp+150 and y < max_samp - 100:
    #    max_samp -= 100
    #elif y > max_samp:
    #    max_samp = y
    #if y > min_samp and y <= max_samp+150 and y > min_samp +100:
    #    min_samp += 100   
    

def draw_text(l,b,screen=screen):
    position = 2
    surfaces = []
    for i,y in enumerate(l['data']):
        r = pg.Rect(2,40*position,155,24)
        screen.fill((0,0,0), r)
        surface = my_font.render('L'+str(position-1) +': '+str(y),False,(127,255,255))
        screen.blit(surface,(0,40*position))
        position += 1
    for i,y in enumerate(b['data']):
        r = pg.Rect(2,40*position,255,24)
        screen.fill((0,0,0), r)
        surface = my_font.render('B:'+str(position-5) +': '+str(y),False,(127,127,255))
        screen.blit(surface,(0,40*position))
        position += 1
    

def draw_lask(packet):
    global count
    global lpps
    global last_lask_packet
    position = 2
    if packet['rec_time']-last_lask_packet['rec_time']>.01:
        lpps = packet['rec_time']-last_lask_packet['rec_time']
        lpps = int(lpps*100)/100
        for i,y in enumerate(last_lask_packet['data']):
            draw_signal(count-2,y,count,packet['data'][i],position,(200,255,255))
            position += 1
        last_lask_packet = packet
    
def draw_prediction(prediction):
    prediction = prediction[0]
    #print(prediction[:4])
    global count
    global lpps
    global last_prediction
    global last_lask_packet
    #print(last_prediction)
    position = 2
    lpps = int(lpps*100)/100
    for i,y in enumerate(prediction[:4]):
        draw_signal(count-2,y,count,y,position,(255,255,0))
        position += 1

def draw_band(packet):
    global count
    global bpps
    global last_band_packet
    position = 6
    if packet['rec_time']-last_band_packet['rec_time']>.01:
        bpps = packet['rec_time']-last_band_packet['rec_time']
        bpps = int(bpps*100)/100
        for i,y in enumerate(last_band_packet['data']):
            draw_signal(count-2,y,count,packet['data'][i],position,(200,200,255))
            position += 1
        last_band_packet = packet

def text_gui(screen=screen):
    global lpps
    global bpps
    global max_samp
    global min_samp
    surface = my_font.render('OpenMuscle Collect Data',False,(255,255,255))
    screen.blit(surface,(0,0))
    r = pg.Rect(2,40,800,24)
    screen.fill((0,0,0), r)
    surface = my_font.render(f'LASK ldp:{lpps} Band ldp:{bpps} SampMAX:{max_samp} SampMIN:{min_samp}',False,(255,200,200))
    screen.blit(surface,(0,40))
    
### File Save Setup
#filenumber = len(os.listdir('../TrainingData/CSV/'))
#file = open(f'../TrainingData/CSV/training_file{filenumber}.txt','w')

# Time Axis Counters
t0 = time.time()
delta_time = 0

# Connection Variables
lask_con = {'active':False,'seq':0}
band_con = {'active':False,'seq':0}

def get_packet(s=s,lask=lask_con,band=band_con):
    packet = False
    s.settimeout(1)
    try:
        data, address = s.recvfrom(4096)
        text = data.decode('utf-8')
        packet = ast.literal_eval(text)
    except:
        pass
    return(packet)

def send_hand(p,maxim,minim):
    fingerRatios = []
    for i in range(4):
        test = (p[i]-minim[i])/(maxim[i]-minim[i])
        if test > .65:
            test = 1
        elif test > .32:
            test = 2/3
        else:
            test = 1/3
        #print(test)
        fingerRatios.append(test)
    drawHand(fingerRatios)
        

######## Main Loop ########
# Haris Turf Hand Vars
ratios=[1/3, 2/3, 3/3]
#---

count = 0
done = False
found_data = []
predictions = []

######### MAX MIN FOR HAND
maxim = [5200,5087,5011,5117]
minim = [4000,4182,4103,4504]
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    pack = get_packet(s)
    # Processes the incoming packet
    # data placed into global found
    if pack:
        pack['rec_time'] = time.time()-t0
        send_chunk(pack)
        check_chunk()
        if len(found_data) < found_count:
            found_data.append(found[-1][0])
        #file.write(str(pack) + '\n')
        # Draw Screen
        #
        if 'OM-Band' in pack['id']:
            draw_band(pack)
            device = 'OpenMuscle Band'
        elif 'OM-LASK' in pack['id']:
            draw_lask(pack)
            device = 'OpenMuscle LASK'
        if found_count % 5 == 0 and found_count > 54:
            input_data = np.array(found_data[-1]).reshape(1, -1)
            last_prediction = loaded_model.predict(input_data)
            send_hand(last_prediction[0],maxim,minim)
            predictions.append(last_prediction[0])
            #print(last_prediction)
            #print(last_lask_packet)
            draw_prediction(last_prediction)
            found_count +=1
    pg.display.update()
    count += 1
    if count > 750:
        screen.fill(0)
        count = 0
    if not count % 100:
        draw_text(last_lask_packet,last_band_packet)
        text_gui()
    # End Draw Screen
    
#file.close()

for i in predictions:
    print(i)

for n in range(5):
    maxim = [max(i) for i in zip(*predictions)][n]
    minim = [min(i) for i in zip(*predictions)][n]
    print(f'Column:{n}   min:{minim}        max:{maxim}')



