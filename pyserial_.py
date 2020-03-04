
import serial
'''
ports = ['COM%s' % (i + 1) for i in range(256)]
results = []
for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        results.append(port)
    except(OSError, serial.SerialException):
        pass

'''
'''
ser = serial.Serial('COM11',baudrate = 9600, timeout = 1)

while 1:
    x = ser.readline()
    print(x)
'''

import time

#portName='/dev/cu.usbmodem1461301'
portName='COM11'
baudRate = 9600

ser = serial.Serial(portName,baudRate)
print("Opening port "+ ser.name)

if ser.is_open==True:
    print("Success!")
else:
    print("Unable to open port :(")

print("Running a demo for 10s...")
startTime = currentTime = int(time.time())

    #decode bytes into string
lineData = []
while abs(currentTime-startTime) < 10:
    bytes = ser.readline()
    line = bytes.decode('utf-8')
    line = line.replace('\r','').replace('\n','')
    print(line)
    lineData.append(line)
    currentTime=int(time.time())
x = []
for d in lineData:
    if 'n' in d:
        print(d)
    else:
        x.append(float(d))
import matplotlib.pyplot as plt

plt.plot(x)
plt.show()
import numpy as np
arr = np.array(x)
np.savetxt('array2.csv', [arr],delimiter=',',fmt='%d')

'''
while abs(currentTime-startTime) < 10:
    ### Below are two demo programs for read from serial. Run only one
    ### of these at a time so additional data is not "accidently" read.

    #### Demo #1 ####
    ## read only a single byte, not really that useful
    #byte = ser.read()
    ## convert to string and strip out all new line characters
    #string = str(byte.decode('utf-8')).replace('\r', '').replace('\n', '')
    #print(string)

    #### Demo #2 ####
    ##read until line and strip out \r\n terminators
    bytes = ser.readline()
    #decode bytes into string
    line = bytes.decode('utf-8')
    line = line.replace('\r','').replace('\n','')
    print(line)

    currentTime=int(time.time())


print("Show's over. Close the port!")
ser.close()
'''
