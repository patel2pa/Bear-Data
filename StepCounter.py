import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import statistics
import serial
import time

'''
Python scripts for finding steps,
some assumptions:
    1)The structure of the data is going to be zero acceleration 
    followed by the step data
    2)The step data is continuous, not break or no interruption  
'''

def get_Data():
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
    '''
    lineData = []
    while abs(currentTime-startTime) < 20:
        bytes = ser.readline()
        line = bytes.decode('utf-8')
        line = line.replace('\r','').replace('\n','')
        print(line)
        lineData.append(line)
        currentTime=int(time.time())
    x = []
    for d in lineData:
        if 'n' in d:
            pass
        else:
            try:
                x.append(float(d))
            except Exception:
                pass
    '''
    lineData = []
    try:
        while True:
            bytes = ser.readline()
            line = bytes.decode('utf-8')
            line = line.replace('\r','').replace('\n','')
            print(line)
            lineData.append(line)
            currentTime=int(time.time())
    except KeyboardInterrupt:
        pass
    x = []
    for d in lineData:
        if len(d)>5:
            x.append(d.split('//'))

    x_1 = []
    for num in x:
        try:
            x_1.append(math.sqrt((int(num[0])*int(num[0]))+(int(num[1])*int(num[1]))+(int(num[2])*int(num[2]))))
        except Exception:
            pass

    arr = np.array(x_1)
    np.savetxt('array3.csv', [arr],delimiter=',',fmt='%d')
    
    return x_1




#gets the data
def getData(fileName):
    data = pd.read_csv(fileName)
    StepData = []
    for d in range(len(data['x'])):
        magnitudeData = (data['x'][d])**2 + (data['y'][d])**2 + (data['z'][d])**2
        StepData.append(math.sqrt(magnitudeData))
    return StepData


#finds the starting and stopping positions
def StartingandStopingPointFinder(SmoothedArray):
    slopChanges = []
    count = 0
    
    while count < (len(SmoothedArray)-5):
        slopChanges.append(statistics.stdev(SmoothedArray[count:count+5]))
        count = count + 5
        
    standerDv = np.array(slopChanges)
    meanOfArray = standerDv.mean()
    
    NonZeros = [0,0]
    zeros = [0,0]
    startingPointFound = False
    endingPointFound = False
    starting = 0
    ending = 0
    
    for num in range(len(slopChanges)):
        if slopChanges[num]<2:          
            if zeros[0] == 2:
                NonZeros[0] = 0
                NonZeros[1] = 0 
            if zeros[1] == 0:    
                zeros[1] = num
            zeros[0] = zeros[0] + 1
            
        elif slopChanges[num]>2:          
            if NonZeros[0] == 2:
                zeros[0] = 0
                zeros[1] = 0
            if NonZeros[1] == 0:
                NonZeros[1] = num
            NonZeros[0] = NonZeros[0] + 1
            
        if NonZeros[0]>5 and startingPointFound == False:
            starting = NonZeros[1]
            startingPointFound = True
        '''
        if zeros[0] > 3 and ((((standerDv[num:]).mean())/meanOfArray) < .70) and startingPointFound == True:
            ending = zeros[1]
            endingPointFound = True
        ''' 
        if endingPointFound == True:
            break

    
    if ending == 0:
        ending = len(slopChanges)-1
    
    return SmoothedArray[starting*5:ending*5], slopChanges, meanOfArray


#positive slop is 1 and negative slop is -1
def getSlop(inputArray):
    array_ = []
    for t in range(len(inputArray)):
        if (inputArray[t] - inputArray[t-1] > 0):
            array_.append(1)
        else:
            array_.append(-1)
    return array_


#Counts the steps
def CountTheOnes(inputArray):
    CountOfOnes = 0
    iterationPlace = 0
    consecutiveOnes  = 0
    
    while iterationPlace < len(inputArray):
        if inputArray[iterationPlace] == 1:
            consecutiveOnes = consecutiveOnes + 1
            iterationPlace = iterationPlace + 1
        elif inputArray[iterationPlace] == -1:
            if consecutiveOnes >= 6:
                CountOfOnes = CountOfOnes + 1
            consecutiveOnes = 0
            iterationPlace = iterationPlace + 1
    return CountOfOnes

arr_1 = [255,253,255,262,253,252,252,250,262,258,254,258,252,256,258,253,252,252,254,256,251,253,257,256,230,303,327,424,512,416,185,103,136,303,569,746,471,247,231,570,592,637,397,182,115,209,485,680,639,316,270,217,247,457,484,638,447,218,119,177,404,617,706,346,277,238,217,447,525,691,415,182,127,177,394,615,688,326,258,267,337,470,533,612,338,197,124,191,498,629,612,328,233,227,236,501,534,594,386,173,126,173,329,614,579,386,265,213,196,311,571,543,596,258,151,122,156,397,632,613,368,229,210,247,460,478,580,487,241,150,143,286,541,742,556,420,345,295,544,633,651,480,224,126,102,236,668,600,493,340,238,222,182,474,550,639,426,204,126,149,355,581,666,390,251,260,213,373,498,588,486,235,139,152,343,575,504,396,291,243,256,323,588,591,588,275,149,119,169,477,631,587,412,251,260,258,453,562,607,476,235,127,122,328,570,686,485,287,266,263,413,528,643,470,198,156,197,385,518,602,512,331,299,438,583,699,502,242,210,192,260,541,735,592,371,312,369,507,646,553,307,153,134,246,531,666,476,282,296,293,418,535,618,422,194,138,175,403,590,635,370,258,257,206,382,564,636,465,198,145,152,364,556,678,404,274,256,306,539,583,606,372,181,139,199,524,605,662,370,273,294,319,570,596,575,287,153,137,214,520,645,633,338,289,261,351,490,595,567,251,192,163,285,563,720,351,273,359,573,401,326,188,183,146,326,221,300,247,299,256,514,249,255,263,258,248,251,256,256,256,247,255,257,249,249,252,257,256,257,251,254,259,256,256,255,252,253,259,253,254,256,254,250,256,254,257,258,249,254,253,261,252,250,251,252,258,255,250,253,255,256,257,255,255,255,254,256,253,252,259,255,254,257,253,256,255,252,253,257,256,254,252,256,255,254,257,259,252,252,255,254,257,257,254,251,253,258,257,254,253,257,252,253,255,257,252,253,255,253,255,253,256,253,256,255,251,254,255,253,254,257,252,258,254,256,254,255,253,258,255,253,255,256,256,254,258,257,254,256,257,257,255,255,253,255,256,255,256,253,255,257,253,258,256,255,254,257,254,254,256,256,254,253,253,258,257,254,255]
#GetData = getData('48_steps.csv')
GetData = get_Data()
GetStartAndStop, standerDV, meanSD = StartingandStopingPointFinder(GetData)
GetSlop = getSlop(gaussian_filter1d(GetStartAndStop, sigma = 3))
GetCount = CountTheOnes(GetSlop)
print('steps count is:', GetCount)

#plt.plot(GetData)
#plt.plot(x_1)
#plt.plot(GetSlop)
#plt.show()


