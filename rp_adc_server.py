
# ADC DMA web server using MicroPython on Pico
#
# For detailed description, see https://iosoft.blog
#
# Copyright (c) 2021 Jeremy P Bentham
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# v0.14 JPB 10/11/21 Tidied up for release

import array, time, uctypes, math, random
import rp_devices as devs, rp_esp32 as esp32

ADC_CHAN = 0
ADC_PIN  = 26 + ADC_CHAN
ADC_SAMPLES = 20
MIN_SAMPLES, MAX_SAMPLES = 10, 1000
ADC_RATE = 100000
MIN_RATE, MAX_RATE = 1000, 500000
DMA_CHAN = 0

DIRECTORY     = "/"
INDEX_HTML    = "rpscope.html"
DATA_CSV      = "data.csv"
CAPTURE_CSV   = "capture.csv"
ICON_ICO      = "favicon.ico"

adc = devs.ADC_DEVICE
dma_chan = devs.DMA_CHANS[DMA_CHAN]
dma = devs.DMA_DEVICE

parameters = {"nsamples":ADC_SAMPLES, "xrate":ADC_RATE, "simulate":0}

# Check if file exists
def file_exists(fname):
    try:
        f = open(fname)
        f.close()
        return True
    except:
        return False
    
# Get filename & parameters from HTML request
def get_fname_params(line, params):
    fname = ""
    params["simulate"] = 0
    parts = line.split()
    if len(parts) > 1:
        p = parts[1].partition('?')
        fname = p[0]
        query = p[2].split('&')
        for param in query:
            p = param.split('=')
            if len(p) > 1:
                if p[0] in params:
                    try:
                        params[p[0]] = int(p[1].replace("on", "1"));
                    except:
                        pass
    return fname

# Initialise ADC DMA
def adc_dma_init():
    pin = devs.GPIO_PINS[ADC_PIN]
    pad = devs.PAD_PINS[ADC_PIN]
    pin.GPIO_CTRL_REG = devs.GPIO_FUNC_NULL
    pad.PAD_REG = 0

    dma.CHAN_ABORT = 0xffff
    dma_chan.CTRL_TRIG_REG = 0

    adc.CS_REG = adc.FCS_REG = 0
    adc.CS.EN = 1
    adc.FCS.EN = adc.FCS.DREQ_EN = 1
    adc.FCS.THRESH = adc.FCS.OVER = adc.FCS.UNDER = 1
    adc.CS.AINSEL = ADC_CHAN

    dma_chan.READ_ADDR_REG = devs.ADC_FIFO_ADDR
    dma_chan.CTRL_TRIG_REG = 0
    dma_chan.CTRL_TRIG.CHAIN_TO = DMA_CHAN
    dma_chan.CTRL_TRIG.INCR_WRITE = dma_chan.CTRL_TRIG.IRQ_QUIET = 1
    dma_chan.CTRL_TRIG.TREQ_SEL = devs.DREQ_ADC
    dma_chan.CTRL_TRIG.DATA_SIZE = 1

# Discard any data in ADC FIFO
def flush_adc_fifo():
    dma_chan.CTRL_TRIG.EN = 0
    while adc.FCS.LEVEL:
        x = adc.FIFO_REG

# Capture ADC samples using DMA
def adc_capture():
    flush_adc_fifo()
    nsamp = max(MIN_SAMPLES, min(MAX_SAMPLES, parameters["nsamples"]))
    rate = max(MIN_RATE, min(MAX_RATE, parameters["xrate"]))
    adc_buff = array.array('H', (0 for _ in range(nsamp)))
    adc.DIV_REG = (48000000 // rate - 1) << 8
    dma_chan.WRITE_ADDR_REG = uctypes.addressof(adc_buff)
    dma_chan.TRANS_COUNT_REG = nsamp
    dma_chan.CTRL_TRIG.EN = 1
    adc.CS.START_MANY = 1
    while dma_chan.CTRL_TRIG.BUSY:
        time.sleep_ms(10)
    adc.CS.START_MANY = 0
    dma_chan.CTRL_TRIG.EN = 0
    return "\r\n".join([("%1.3f" % (val*3.3/4096)) for val in adc_buff])

# Simulate ADC samples: sine wave plus noise
def adc_sim():
    nsamp = parameters["nsamples"]
    buff = array.array('f', (0 for _ in range(nsamp)))
    f, s, c = nsamp/20.0, 1.0, 0.0
    for n in range(0, nsamp):
        s += c / f
        c -= s / f
        val = ((s + 1) * (c + 1)) + random.randint(0, 100) / 300.0
        buff[n] = val
    return "\r\n".join([("%1.3f" % val) for val in buff])

esp = esp32.server_init()
adc_dma_init()

while True:
    req = esp.get_http_request()
    if req:
        #print(req)
        line = req.split("\r")[0]
        fname = get_fname_params(line, parameters)
        print(line, end="")
        if ICON_ICO in fname:
            print(": not found")
            esp.put_http_404()
        elif DATA_CSV in fname:
            print(": data file")
            esp.put_http_file(DIRECTORY+DATA_FNAME, "text/csv", esp32.DISABLE_CACHE)
        elif CAPTURE_CSV in fname:
            print(": capture CSV")
            vals = adc_sim() if parameters["simulate"] else adc_capture()
            esp.put_http_text(vals, "text/csv", esp32.DISABLE_CACHE)
        elif file_exists(fname):
            print(": file %s" % fname)            
            esp.put_http_file(fname)
        else:
            print(": index file")
            esp.put_http_file(DIRECTORY+INDEX_HTML)
        #if parameters:
        #    print("Parameters: " + str(parameters))
    time.sleep_ms(10)
# EOF


