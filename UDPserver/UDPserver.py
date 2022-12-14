#!python3

import socket
import sys
import numpy as np
import time
import pygame as pg
import csv
import os

def calibrate(data):
    calib = []
    for i in data:
        calib.append(int(i))
    return calib

def plotAdjust(data,factor=4):
    adjusted = []
    for i in data:
        adjusted.append(i/factor)
    return adjusted

#get Local IP Address
#Taken from https://stackoverflow.com/questions/24196932
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    return s.getsockname()[0]

ip_address = get_ip_address()
print(f"ipaddress: {ip_address}")

#pygame width height etc
WIDTH = 1200
HEIGHT = 800

#pygame init and screen declaration
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH,HEIGHT))


#Command LIne parameters
if len(sys.argv) == 3:
    #Get "IP address of Server" and also the "port number" from arg 1 and 2
    ip = sys.argv[1]
    port = int(sys.argv[2])
else:
    print('run like: python UDPserver.py <arg1: server ip> <arg2: UDPport>')
    ip = ip_address
    port = 3145
    print('using {0} and 3145 '.format(ip_address))

# Create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (ip, port)
s.bind(server_address)
print('Do Ctrl+c to exti the program !!')

y = 0
x = 0
olds = [0,0,0,0,0,0,0,0,0,0,0,0]
pg.font.init()
my_font = pg.font.SysFont('Courier New', 24)

# distance per line
adc_dis = 65
# magnidute of signal Pop Pop!
pop = 4
buff = 25

# Data save file in CSV format

filenumber = len(os.listdir('../TrainingData/CSV/'))
data_file = open(f'../TrainingData/CSV/training_file{filenumber}.csv','w')
writer = csv.writer(data_file)

text_surface = my_font.render('here we go!', False, (127,127,127))
screen.blit(text_surface, (200,200))
pg.display.update()

first_run = True
calib = [0,0,0,0,0,0,0,0,0,0,0,0]

done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE: done = True
        elif event.type == pg.QUIT:
            data_file.close()
            done = True
    #print('heellllllooooo')
    data, address = s.recvfrom(4096)
    text = data.decode('utf-8')
    print('text: ',text)
    writer.writerow(text.split(','))
    print(text)
    better = text.split(',')
    better = better[:-1]
    #pygame loop screen refresh etc
    #screen.fill(0)
    ints = []
    oo = 0
    if first_run:
        calib = calibrate(better)
        first_run = False
    for c, i in enumerate(better):
        ints.append(int((int(i)-calib[c])/pop))
    lines = []
    for i in ints:
        #pg.draw.line(screen,(255,255,255),(x*2,olds[oo]+oo*adc_dis+buff),(x*2,i+oo*adc_dis+buff),width=2)
        lines.append([(x*2,olds[oo]+oo*adc_dis+buff),(x*2,i+oo*adc_dis+buff)])
        oo += 1
    if lines or ints:
        pg.draw.line(screen,(255,0,255),lines[0][0],lines[0][1],width=2)
        pg.draw.line(screen,(255,0,255),lines[6][0],lines[6][1],width=2)
        pg.draw.line(screen,(255,0,0),lines[1][0],lines[1][1],width=2)
        pg.draw.line(screen,(255,0,0),lines[7][0],lines[7][1],width=2)
        pg.draw.line(screen,(255,127,0),lines[2][0],lines[2][1],width=2)
        pg.draw.line(screen,(255,127,0),lines[8][0],lines[8][1],width=2)
        pg.draw.line(screen,(0,127,255),lines[3][0],lines[3][1],width=2)
        pg.draw.line(screen,(0,127,255),lines[9][0],lines[9][1],width=2)
        pg.draw.line(screen,(0,255,0),lines[4][0],lines[4][1],width=2)
        pg.draw.line(screen,(0,255,0),lines[10][0],lines[10][1],width=2)
        pg.draw.line(screen,(255,255,0),lines[5][0],lines[5][1],width=2)
        pg.draw.line(screen,(255,255,0),lines[11][0],lines[11][1],width=2)
        olds = ints
    clock.tick(60)
    x += 1
    pg.display.update()
    # Every 10 draws show text on the screen
    if not x%10:
        surfaces = []
        oo = 0
        for i in ints:
            try:
                number = str(i)
                r = pg.Rect(20,adc_dis*oo,255,24)
                screen.fill((0,0,0), r)
                if oo > 5:
                    position = 'top'
                else:
                    position = 'bot'
                surfaces.append(my_font.render('Cell:'+str(((oo+1)%6)-1)+position+' ' +str(number),False,(127,255,255)))
                screen.blit(surfaces[oo], (25,adc_dis*oo))
            except:
                print('could not draw text')

            oo += 1
    if x > 600:
        screen.fill(0)
        x = 0
    for event in pg.event.get():
        if event.type==pg.QUIT:
            data_file.close()
            try:
                data_file.close()
            except:
                print("failed to close data_file a second time")
            done = True
            pg.quit()
            exit(0)
    #print("\n\n 2. Server received: ", data.decode('utf-8'), "\n\n")
    #send_data = input("type some text to send => ")
    #s.sendto(send_data.encode('utf-8'), address)
    #print("\n\n 1. Server sent: ", send_data, "\n\n")
    
    
