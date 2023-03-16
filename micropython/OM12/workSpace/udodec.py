#udodec.py


import neopixel
import machine
import time
print('hello world!')

np = neopixel.NeoPixel(machine.Pin(39),300)

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
sequence = 'RLLRLLLLBLL'

edges = []
for i in range(31):
  edges.append([i,0])


def run_once(np=np):
  for i in range(300):
    np[i] = (255,127,0)
    np.write()
    time.sleep(.01)
    np[i] = (0,0,0)
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
  
  
  
# have to give it directions:pattern and how many times:runs
def iterate_route(pattern,spaces,cur_pos = -1,verts=verts,np=np):
  pat = convert_directions(pattern)
  print(f'Pattern Numeric Array:{pat}')
  for r in range(runs):
    for p in pat:
      if cur_pos > 0:
        color = change_color(cur_pos,np[(cur_pos*10)-10])
      else:
        color = change_color(cur_pos,np[(-cur_pos*10)-10])
      for y in range(10):
        if cur_pos > 0:
          cur_pos[(cp*10)-10+y] = color
        elif cur_pos < 0:
          np[(-cur_pos*10)-10+(9-y)] = color
        np.write()
        #time.sleep(.01)
      #Pattern code
      found = False
      for i,x in enumerate(verts):
        if -cur_pos in x and not found:
          print(f'cur_pos:{cur_pos}',f'Vertici:{x}',f'pattern:{p}')
          indie = x.index(-cur_pos)
          cur_pos = x[indie+p]
          print(f'new cur_pos:{cur_pos} indie:{indie} p:{p}')
          found = True
          
def move_pixel(pattern,runs,verts=verts,np=np):
  pos = -1
  pat = convert_directions(pattern)
  print(f'Pattern Numeric Array:{pat}')
  for r in range(runs):
    for p in pat:
      if cp > 0:
        color = change_color(pos,np[(pos*10)-10])
      else:
        color = change_color(pos,np[(-pos*10)-10])
      for y in range(10):
        if pos> 0:
          np[(pos*10)-10+y] = color
        elif pos < 0:
          np[(-pos*10)-10+(9-y)] = color
        np.write()
        #time.sleep(.01)
      #Pattern code
      found = False
      for i,x in enumerate(verts):
        if -pos in x and not found:
          print(f'pos:{pos}',f'Vertici:{x}',f'pattern:{p}')
          indie = x.index(-cp)
          pos = x[indie+p]
          print(f'new pos:{pos} indie:{indie} p:{p}')
          found = True
 

print('right before!')
iterate_route('RLLRLLLLBLL',50)

      
      
    
    
  
