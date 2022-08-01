import serial
import time
import re 
from datetime import datetime

ser = serial.Serial('/dev/ttyACM0',baudrate = 115200, timeout = 1)
ser.reset_input_buffer()

def current_milli_time():
    return round(time.time() * 1000)
t=0
while True:
    if ser.in_waiting > 0:
        # timest = current_milli_time()
        # # data = ser.readline().decode('ascii').rstrip()
        data = ser.readline().decode('ascii',errors='ignore').rstrip()
        data1_split = data.split(',') 
        # print (len(data1_split))
        # print (data1_split)
        
           
        # if len(data1_split) < 4:
        #     print ('index error')
        # else:
        #     if re.match(r'^-?\d+(?:\.\d+)$', data1_split[1]) is None and re.match(r'^-?\d+(?:\.\d+)$', data1_split[2]) is None:
        #         print('noise')
        #         print(f'{timest},{data}')
        #         print('lat ='+data1_split[1]+', long ='+data1_split[2])
        #     else:
        #         print(f'{timest},{data}')
        #         print('lat ='+data1_split[1]+', long ='+data1_split[2])
         
        now = datetime.now()
        dt_string = now.strftime("%M")
        
        if (t == 0 or int(dt_string) == 0):
            t = int(dt_string) 
            print('set time to:'+str(t))
        elif (int(dt_string) - t >= 1):
            t = int(dt_string)
            # data = ser.readline().decode('ascii').rstrip()
            # data1 = ser1.readline().decode('ascii',errors='ignore').rstrip()
            data1_split = data.split(',') 
            if len(data1_split) < 4:
                print ('index error')
                print(data)
            else:
                if re.match(r'^-?\d+(?:\.\d+)$', data1_split[1]) is None and re.match(r'^-?\d+(?:\.\d+)$', data1_split[2]) is None:
                    print('noise')
                    # print(f'{timest},{data}')
                    print('lat ='+data1_split[1]+', long ='+data1_split[2])
                else:
                    val = 'loc,'+str(current_milli_time())+','+data
                    # value = write_read(val)
                    print(val)
            print('time change to:'+str(t))
        elif(t > 0):
            print('time now:'+str(t))