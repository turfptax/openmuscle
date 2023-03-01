#udodec.py


import neopixel
import machine
import time
import gc
import random
print('hello world!')

np = neopixel.NeoPixel(machine.Pin(39),300)
for i in range(300):
  np[i] = (10,10,10)
np.write()

for i in range(300):
  np[i] = (0,0,0)
np.write()

verts= [[-1,2,3],
[-3,4,5],
[-5,6,7],
[-7,8,9],
[-9,10,1],
[-4,-17,18],
[-14,15,-2],
[-10,11,12],
[-8,-23,24],
[-6,-20,21],
[20,-18,19],
[17,-15,16],
[14,-12,13],
[-11,-24,25],
[23,-21,22],
[-19,-29,30],
[29,-16,-28],
[28,-13,-27],
[27,-25,26],
[-26,-22,-30]] 

faces = [
[1,3,5,7,-9],
[9,8,24,-11,-10],
[-8,-7,6,21,23],
[6,-20,-18,4,5],
[-4,-3,2,15,17],
[-2,-1,10,12,14],
[-12,11,25,27,-13],
[13,28,-16,-15,-14],
[16,29,-19,-18,-17],
[19,30,-22,-21,-20],
[22,-26,-25,-24,-23],
[26,-30,-29,-28,-27]]

sequence = 'RLLRLLLLBLL'
tracers = False
die_rate = 20
pixel = []

def run_once(np=np):
  for i in range(300):
    np[i] = (255,127,0)
    np.write()
    time.sleep(.01)
    np.buf = bytearray(900)
    np.write()
  return
  
  
def count_edges(np=np):
  for i in range(30):
    for a in range(10):
      np[(i*10)+a] = (127,127,255)
    np.write()
    time.sleep(1)
    print(f'group:{i*10}-{((i+1)*10)-1}')
    input()
    for a in range(10):
      np[(i*10)+a] = (27,0,0)
    np.write()
    
    
    
def convert_directions(text):
  numeric = []
  for i in text:
    if i == 'R':
      numeric.append(-2)
    if i == 'L':
      numeric.append(-1)
    if i == 'B':
      numeric.append(-3)
  return numeric
  
def change_color(cp,rgb):
  global edges
  hits = edges[abs(cp)][1]
  new_rgb = [0,0,0]

  new_rgb[hits%3] += 11
  r = rgb[0] + new_rgb[0]
  g = rgb[1] + new_rgb[1]
  b = rgb[2] + new_rgb[2]
  edges[abs(cp)][1] += 1
  return (r,g,b)
  
  
 
def dim(die_rate=die_rate,np=np):
  for i in range(len(np)):
    if np[i][0] + np[i][1] + np[i][2] > 0:
      r = np[i][0] - die_rate
      g = np[i][1] - die_rate
      b = np[i][2] - die_rate
      if r < 0:
        r = 0
      if g < 0:
        g = 0
      if b < 0:
        b = 0
      np[i] = (r,g,b)

    
def move(verts=verts,np=np):
  global tracers
  global pixel
  newp = None
  gc.collect()
  newp = []
  np.buf = bytearray(900)
  for p in pixel:
    edge = p[0]
    pix = p[1]
    l = p[2]
    speed = p[3]
    pattern = p[4]
    adjustment = p[5]
    ttl = p[6]
    pat = convert_directions(pattern)
    found = False
    for num in range(speed):
        if pix + 1 > 9:
          ttl -= 1
          for i,x in enumerate(verts):
            if -edge in x and not found:
              #print(f'edge:{edge}',f'Vertici:{x}',f'pattern:{p}')
              indie = x.index(-edge)
              edge = x[indie+pat[0]]
              #print(f'new edge:{edge} indie:{indie} pat[0]:{pat[0]}')
              found = True
          pattern = pattern[1:] + pattern[0]
          pix = pix + 1 - 10
        else:
          pix = pix + 1
        if edge > 0:
          np[(edge*10)-10+pix] = adjustment
        elif edge < 0:
          np[(-edge*10)-10+(9-pix)] = adjustment
    if ttl != 0:
      newp.append([edge,pix,l,speed,pattern,adjustment,ttl])
  np.write()
  pixel = newp


print('right before!')
#iterate_route('RLLRLLLLBLL',50)

pixel.append([i,0,1,3,'RLLRLLLLBLL',(r,g,b),-1])

for i in range(1000):
  move()

