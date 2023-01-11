import socket
import numpy as np
import pygame as pg
import csv
import sys
import os
import time
import ast

last_lask_packet = {'id': 'OM-LASK4', 'time': (2023, 1, 8, 22, 37, 28, 6, 8), 'data': [-591, -667, -747, -457], 'ticks': 53249, 'rec_time': 0.0001}
last_band_packet = {'id': 'OM-Band12', 'time': (2023, 1, 8, 22, 37, 28, 6, 8), 'data': [4928, 4828, 4824, 4992, 4673, 4897, 4993, 4805, 5020, 6829, 4400, 5349], 'ticks': 356392, 'rec_time': 0.0001}

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
pg_width = 800
pg_height = 800

#pygame init and screen declaration
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((pg_width,pg_height))

text_surface = my_font.render('OpenMuscle', False, (127,127,127))
screen.blit(text_surface, (200,200))
pg.display.update()

first_run = True
adc_dis = 65
pop = 4
buff = 25

def draw_signal(x0,y0,x,y,position,screen=screen):
    height = 40
    max_samp = 6500
    # Row Multiply by position # * pixel height
    y0 = int((y0/max_samp)*40)+(position*40)
    y = int((y/max_samp)*40)+(position*40)
    # Left Padding
    x += 50
    x0 += 50
    pg.draw.line(screen,(255,0,255),(x0,y0),(x,y),width=1)

def draw_lask(packet,last_packet=last_lask_packet):
    global count
    global last_lask_packet
    position = 0
    if packet['rec_time']-last_packet['rec_time']>.1:
        for i,y in enumerate(last_packet['data']):
            draw_signal(count-1,y,count,packet['data'][i],position)
            position += 1
        last_lask_packet = packet
    
    

def draw_band(packet,last_packet=last_band_packet):
    global count
    global last_band_packet
    position = 4
    if packet['rec_time']-last_packet['rec_time']>.1:
        for i,y in enumerate(last_packet['data']):
            draw_signal(count-1,y,count,packet['data'][i],position)
            position += 1
        last_band_packet = packet
    
### File Save Setup
filenumber = len(os.listdir('../TrainingData/CSV/'))
file = open(f'../TrainingData/CSV/training_file{filenumber}.txt','w')

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

######## Main Loop ########
count = 0
done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            data_file.close()
            done = True
    pack = get_packet(s)
    if pack:
        pack['rec_time'] = time.time()-t0
        file.write(str(pack) + '\n')
        # Draw Screen
        #
        if 'OM-Band' in pack['id']:
            draw_band(pack)
            device = 'OpenMuscle Band'
        elif 'OM-LASK' in pack['id']:
            draw_lask(pack)
            device = 'OpenMuscle LASK'
    pg.display.update()
    count += 1
    if count > 750:
        screen.fill(0)
        count = 0
    # End Draw Screen
    
    
    
data_file.close()





