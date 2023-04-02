# txt to csv
# convert txt json data to csv for ml
import csv


found = []
lask = []
band = []
last_pair = None

def send_chunk(data):
    global lask
    global band
    temp = []
    # array structure [signal_int * count,received time float]
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
    dindexL =[]
    dindexB =[]
    if len(band) > 10:
        for i,x in enumerate(band):
            time = x[-1]
            for o,z in enumerate(lask):
                if abs(z[-1] - time) < .02:
                    found.append([x,z])
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

text_file = open('capture_11.txt','r')
csv_file = open('capture_010.csv','w',newline="") #added newline="" FYI FMI
writer = csv.writer(csv_file)
writer.writerow(['OM1','OM2','OM3','OM4','OM5','OM6','OM7','OM8','OM9','OM10','OM11','OM12','om_time','LASK1','LASK2','LASK3','LASK4','lask_time'])
             
matched_pairs = []                    
for i in text_file.read().split('\n'):
    #print(i)
    try:
        j = eval(i)
    except:
        print(i,'failed to eval()')
    send_chunk(j)
    check_chunk()

print('finished matching')

for i in found:
    writer.writerow(i[0] + i[1])

csv_file.close()
        
    
    


    



