import serial 
import re


ser = serial.Serial('COM6',baudrate = 115200, timeout = 1)
ser.reset_input_buffer()

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('ascii',errors = 'ignore').rstrip()
        data_split = data.split(',')
        # //////////////////// DEVICE /////////////////////////////////////////////////////////////
        device1 = {'guid':'cccf5d68-3a56-496a-a5b3-380ad86af737', 'lat': 00, 'long': 00, 'RSSI':00}
        #//////////////////////////////////////////////////////////////////////////////////////////
        if len(data_split) == 4:

            if re.match(r'^-?\d+(?:\.\d+)$', data_split[1]) is None and re.match(r'^-?\d+(?:\.\d+)$', data_split[2]) is None and data_split[1] != 'Invalid':

                if data_split[0] == 'cccf5d68-3a56-496a-a5b3-380ad86af737':
                    device1['lat'] = data_split[1]
                    device1['long'] = data_split[2]
                    device1['RSSI'] = data_split[3]
                    val = 'loc,'+str(device1.get('guid'))+','+str(device1.get('lat'))+','+str(device1.get('long'))+','+str(device1.get('RSSI'))
                    print (val)


            else: print('invalid data == '+data)
        else:  
            print('index error == '+data)


        