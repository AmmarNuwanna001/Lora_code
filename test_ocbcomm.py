import serial 
ser = serial.Serial('/dev/ttyUSB0',baudrate = 9600, timeout = 1)
ser.reset_input_buffer()
x = 'Check orbcomm'
ser.write(bytes(x, 'utf-8'))
print(x)

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('ascii').rstrip()
        print(data)