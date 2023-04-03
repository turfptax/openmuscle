import socket
import numpy as np
import pygame as pg
import csv
import sys
import os
import time
import ast

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
    #if y < max_samp and y >= min_samp+150 and y < max_samp - 100:
    #    max_samp -= 100
    #elif y > max_samp:
    #    max_samp = y
    #if y > min_samp and y <= max_samp+150 and y > min_samp +100:
    #    min_samp += 100   
    pg.draw.line(screen,color,(x0,y0),(x,y),width=1)

def draw_text(l,b,screen=screen):
    position = 2
    surfaces = []
    for i,y in enumerate(l['data']):
        r = pg.Rect(2,40*position,255,24)
        screen.fill((0,0,0), r)
        surface = my_font.render('LASK: '+str(position) +': '+str(y),False,(127,255,255))
        screen.blit(surface,(0,40*position))
        position += 1
    for i,y in enumerate(b['data']):
        r = pg.Rect(2,40*position,255,24)
        screen.fill((0,0,0), r)
        surface = my_font.render('BAND: '+str(position) +': '+str(y),False,(127,127,255))
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
#filenumber = len(os.listdir('Data-Captures/'))
file = open(f'Data-Captures/live_capture.txt','w')

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
            file.close()
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
    if not count % 100:
        draw_text(last_lask_packet,last_band_packet)
        text_gui()
    # End Draw Screen
    
    
    
file.close()





