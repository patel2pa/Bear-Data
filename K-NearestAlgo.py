#from sklearn.neighbors import KNeighborsClassifier as Knn
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
'''
x = [[0,0,0], [1,1,1], [2,2,2]]
y = [0,1,0]


z = Knn(n_neighbors = 1)
z.fit(x,y)
print(z.predict([[1,1,1]]))
'''

def getData(fileName):
    data = pd.read_csv(fileName)
    StepData = []
    for d in range(len(data['x'])):
        magnitudeData = (data['x'][d])**2 + (data['y'][d])**2 + (data['z'][d])**2
        StepData.append(math.sqrt(magnitudeData))
    return StepData

#GetData = getData("14_steps.csv")
#plt.plot(GetData)
#plt.show()

Data = getData("14_steps.csv")
Data = gaussian_filter1d(Data, sigma = 3)
Total_Length = len(Data)


array = []
count = 0
currentArray = []

for num in range(Total_Length):
    if count == 20:
        array.append(currentArray)
        currentArray = []
        count = 0
    else:
        currentArray.append(Data[num])
        count = count + 1
X = np.array(array)


maginitude = []
for x in X:
    maginitude.append(int(np.linalg.norm(x)))
#nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
#dis, ind = nbrs.kneighbors(X)


kmean = KMeans(n_clusters=2, random_state=0).fit(np.array(maginitude).reshape(-1,1))




