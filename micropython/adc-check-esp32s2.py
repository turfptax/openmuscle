


# Test ADC ESP32-S2 mini wemos
# getting the ADCs configured for Capicitors
# Some channels are noisy and GPIO 17
# On OpenMuscle 5.3.0 won't register'

import uerrno
import machine
import time
#Setup basic ADC pin read array test
print('setting up 4 hall array: hall[0-18]')
hall = []
for i in range(1,19):
  temp = machine.ADC(Pin(i))
  #important to read the value properly
  temp.atten(ADC.ATTN_11DB)
  hall.append(temp)


def run_adc(h,t=10):
  val = 0
  sums = [0,0]
  print(f't:{t}')
  for i in range(t):
    signal = h.read()
    uvolts = h.read_uv()
    ratio = int(uvolts/signal)
    time.sleep(.3)
    sums[0] += signal
    sums[1] += uvolts
    print(f'uVolts: {uvolts} signal:{signal} ratio:{ratio}')
  ave_signal = int(sums[0]/t)
  ave_volts = int(sums[1]/t)
  print(f'average signal:{ave_signal} volts:{ave_volts}')
  print(ave_volts/ave_signal)

run_adc(hall[15],10)
print('---------')
run_adc(hall[16],10)


def run_all(h = hall):
  for i in range(len(h)):
    print(f'h[{i}]:{h[i].read()}')










