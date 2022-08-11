import serial 
import time
import threading
import re
from datetime import datetime




ser1 = serial.Serial('COM6',baudrate = 115200, timeout = 1)
ser1.reset_input_buffer()



# //////////////////// DEVICE /////////////////////////////////////////////////////////////
device1 = {'loc':'loc','timestamp':00,'guid':'cccf5d68-3a56-496a-a5b3-380ad86af737', 'lat': 00, 'long': 00, 'RSSI':00}
device2 = {'loc':'loc','timestamp':00,'guid':'e1a57058-c970-42d6-9dc5-029c87f72bda', 'lat': 00, 'long': 00, 'RSSI':00}
#//////////////////////////////////////////////////////////////////////////////////////////

def current_milli_time():
    return round(time.time() * 1000)


def sendData(index0,index1,index2,index3,indexLength,rawData):
    val1 , val2 = 'val1' , 'val2'
    h , j = 0 , 0
    if  indexLength == 4:
        # if re.match(r'^-?\d+(?:\.\d+)$', data_split[1]) is not None and re.match(r'^-?\d+(?:\.\d+)$', data_split[2]) is not None and data_split[1] != 'Invalid':
        if re.match(r'^-?\d+(?:\.\d+)$', index1) is not None and re.match(r'^-?\d+(?:\.\d+)$', index2) is not None :
            if device1['guid'] == index0 and h == 0:
                device1['timestamp'] = str(current_milli_time())
                device1['lat'] = index1
                device1['long'] = index2
                device1['RSSI'] = index3
                val1 = device1.get('loc')+','+str(device1.get('timestamp'))+','+str(device1.get('guid'))+','+str(device1.get('lat'))+','+str(device1.get('long'))+','+str(device1.get('RSSI'))
                # global val1
                print (val1)
                h =h+1
                j=0
            elif device2['guid'] == index0 and j == 0:
                device2['timestamp'] = str(current_milli_time())
                device2['lat'] = index1
                device2['long'] = index2
                device2['RSSI'] = index3
                val2 = device2.get('loc')+','+str(device2.get('timestamp'))+','+str(device2.get('guid'))+','+str(device2.get('lat'))+','+str(device2.get('long'))+','+str(device2.get('RSSI'))
                # global val2
                print (val2)
                j = j+1
                h=0
            return val1,val2 
        else: 
            print('invalid data == '+rawData)
            val1 = 'invalid'
            val2 = 'invalid'
    else:  
        print('index error == '+rawData)
        val1 = 'index error'
        val2 = 'index error'
    
    
t = 0
count = 0         
while True:
    if ser1.in_waiting > 0:
        data = ser1.readline().decode('ascii',errors='ignore').rstrip()
        data_split = data.split(',')
        if len(data_split) == 4:
            now = datetime.now()
            dt_string = now.strftime("%M")
            if (t == 0 or int(dt_string) == 0):
                t = int(dt_string)
                print('set time to:'+str(t))
                sendData(data_split[0],data_split[1],data_split[2],data_split[3],len(data_split),data) 
                # count = count + 1
            elif (int(dt_string) - t >= 1):
                t = int(dt_string)
                print('time change to:'+str(t))
                result = sendData(data_split[0],data_split[1],data_split[2],data_split[3],len(data_split),data)
                # for x in len(v):
                #     # if v[i] != 0:
                # print(type(v))
                print(result)

            elif(t > 0 ):
                print('time now:'+str(t))
                sendData(data_split[0],data_split[1],data_split[2],data_split[3],len(data_split),data) 


 

        
