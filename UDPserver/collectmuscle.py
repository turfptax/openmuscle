import socket
import numpy as np
import pygame as pg
import csv
import sys
import os


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
    print('using {0} and 3145 '.format(ip_address))


### Create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (local_ip, port)
s.bind(server_address)
print(f'Server Address:{local_ip} Port:{port}')
print('Do Ctrl+c to exti the program !!')


### File Save Setup
filenumber = len(os.listdir('../TrainingData/CSV/'))
data_file = open(f'../TrainingData/CSV/training_file{filenumber}.csv','w')
writer = csv.writer(data_file)

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


######## Main Loop ########
done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE: done = True
        elif event.type == pg.QUIT:
            data_file.close()
            done = True
    






