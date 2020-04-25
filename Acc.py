from numpy import dstack
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import to_categorical
from matplotlib import pyplot
from pandas import read_csv
import numpy as np
from numpy import dstack
from matplotlib import pyplot as plt
import os

def loaded_file(filepath):
    dataframe = read_csv(filepath, header=None, delim_whitespace=True)
    return dataframe.values

def loaded_data(fileName):
    group = fileName 
    filepath = group + '/Inertial Signals/'
    filenames = list()
    filenames += ['total_acc_x_'+group+'.txt', 'total_acc_y_'+group+'.txt', 'total_acc_z_'+group+'.txt']
    #filenames += ['body_acc_x_'+group+'.txt', 'body_acc_y_'+group+'.txt', 'body_acc_z_'+group+'.txt']
    filenames += ['body_gyro_x_'+group+'.txt', 'body_gyro_y_'+group+'.txt', 'body_gyro_z_'+group+'.txt']

    loaded = list()
    
    for name in filenames:
        data = loaded_file(filepath+name)
        loaded.append(data)

    return loaded
        
loaded = loaded_data('test')
loaded_train = loaded_data('train')


dsloaded_train = dstack(loaded_train)
dsloaded = dstack(loaded)

y_test = loaded_file('test' + '/y_test.txt')
y_train = loaded_file('train' + '/y_train.txt')

def loaded_dataset(trainX, trainY, testX, testY):
    trainY = trainY - 1
    testY = testY - 1
    trainY = to_categorical(trainY)
    testY = to_categorical(testY)
    return trainX, trainY, testX, testY

trainX, trainy, testX, testy = loaded_dataset(dsloaded_train, y_train,dsloaded, y_test)

verbose, epochs, batch_size = 0, 15, 64
n_timesteps, n_features, n_outputs = trainX.shape[1], trainX.shape[2], trainy.shape[1]
model = Sequential()
model.add(LSTM(100, input_shape=(n_timesteps,n_features)))
model.add(Dropout(0.5))
model.add(Dense(100, activation='relu'))
model.add(Dense(n_outputs, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(trainX, trainy, epochs=epochs, batch_size=batch_size, verbose=verbose)
_, accuracy = model.evaluate(testX, testy, batch_size=batch_size, verbose=0)

model.save(os.path.join('.',"test.h5"))

