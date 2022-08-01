import serial 
import time
import threading
import re
import RPi.GPIO as GPIO
from datetime import datetime
from gpiozero import LED


ser = serial.Serial('/dev/ttyUSB0',baudrate = 9600, timeout = 1)
ser1 = serial.Serial('/dev/ttyACM0',baudrate = 115200, timeout = 1)
ser.reset_input_buffer()
ser1.reset_input_buffer()

def current_milli_time():
    return round(time.time() * 1000)

def write_read(x):
    ser.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = ser.readline()
    return data
# def isfloat(num):
#     try:
#       float(num)
#       return True
#     except Exception:
#       pass

led = LED(17)
t = 0

while True:
    if ser1.in_waiting > 0:
        data = ser.readline().decode('ascii').rstrip()
        data1 = ser1.readline().decode('ascii',errors='ignore').rstrip()

        # now = datetime.now()
        # dt_string = now.strftime("%M")
        # if (t == 0 or int(dt_string) == 0):
        #     t = int(dt_string) 
        #     print('set time to:'+str(t))
        # elif (int(dt_string) - t >= 2):
        #     t = int(dt_string)
        #     data = ser.readline().decode('ascii').rstrip()
        #     data1 = ser1.readline().decode('ascii',errors='ignore').rstrip()
        #     val = 'loc,'+str(current_milli_time())+','+data1
        #     value = write_read(val)
        #     print(val)
        #     print('time change to:'+str(t))
        # elif(t > 0):
        #     # print('time now:'+str(t))
            




        # printit()
        # x = input("Y/N: ")
        # if x == 'y':
        #     data = ser.readline().decode('ascii').rstrip()
        #     data1 = ser1.readline().decode('ascii',errors='ignore').rstrip()
        #     val = 'loc,'+str(current_milli_time())+','+data1
        #     value = write_read(val)
        #     print(val)
            
        # else:
        #     print('sleep')
        #     data1 = ser1.readline().decode('ascii',errors='replace').rstrip()
        #     val = 'loc,'+str(current_milli_time())+','+data1
        #     print(val)
            # time.sleep(3)
   
        # x = input("Y/N: ")
        # if x == 'y':
        #     data = ser.readline().decode('ascii').rstrip()
        #     data1 = ser1.readline().decode('ascii',errors='ignore').rstrip()
        #     val = 'loc,'+str(current_milli_time())+','+data1
        #     value = write_read(val)
        #     print(val)
            
        # else:
        #     print('sleep')
        #     data1 = ser1.readline().decode('ascii',errors='replace').rstrip()
        #     val = 'loc,'+str(current_milli_time())+','+data1
        #     print(val)
        
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
            led.on()
        elif (int(dt_string) - t >= 1):
            t = int(dt_string)
            # data = ser.readline().decode('ascii').rstrip()
            # data1 = ser1.readline().decode('ascii',errors='ignore').rstrip()
            data1_split = data1.split(',') 
            if len(data1_split) < 4:
                print ('index error')
                print(data1)
                led.off()
                time.sleep(0.5)
            else:
                if re.match(r'^-?\d+(?:\.\d+)$', data1_split[1]) is None and re.match(r'^-?\d+(?:\.\d+)$', data1_split[2]) is None:
                    print('noise')
                    # print(f'{timest},{data}')
                    print('lat ='+data1_split[1]+', long ='+data1_split[2])
                    led.off()
                    time.sleep(0.5)
                    
                else:
                    val = 'loc,'+str(current_milli_time())+','+data1
                    value = write_read(val)
                    print(val)
            print('time change to:'+str(t))
        elif(t > 0):
            print('time now:'+str(t))
            led.on()

 

        
